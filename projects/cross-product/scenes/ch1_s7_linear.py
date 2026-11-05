"""Chapter 1, scene 7: every step keeps sums, so a x (b + c) = a x b + a x c. Clips c1.lin.1 - c1.lin.4.

A ThreeDScene: 3D things live in scene space (s4 coordinates mapped by P so that a points up),
everything flat (strip, labels, equations) is fixed in frame (see `hud`).

HAND-OFF FROM s6 (ch1_s6_machine): the block "s6 hand-off" below (S6_CAM, make_a, make_floor,
Strip, question_eq) is the only place that has to match s6's end shot. The scene opens on exactly
that shot and glides to its own views at {feed}.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene as FlatNarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# ── s6 hand-off ──────────────────────────────────────────────────────────────────────────────
U = 1.0                      # scene units per s4 unit


def P(v):
    """s4 coordinates (a = (3, 0, 0)) -> scene point. A cyclic swap (right-handed): s4 x is up."""
    x, y, z = v
    return U * np.array([y, z, x], dtype=float)


A_VEC = (3, 0, 0)
A_LBL_OFF = 0.35 * RIGHT     # a's label: this far from a's tip on screen
# s6's end shot (its A_UP view in this frame): origin at screen (-0.3, -0.2), a's tip at (-0.32, 1.40)
S6_CAM = dict(phi=40 * DEGREES, theta=50 * DEGREES, gamma=0, zoom=0.78, focal_distance=33.33,
              frame_center=(-0.4209, 0.0968, 0.1648))
S6_UNIT = 0.6                # s6's scene units per s4 step (its 3D arrow sizes are in those)


def s6_vec3(end, color, start=(0, 0, 0), thick=0.025, tip_h=0.27, tip_r=0.095):
    """s4/s6's 3D vector (Line3D shaft + Cone tip, flat colour), sizes given in s6 units."""
    k = U / S6_UNIT
    start, end = np.asarray(start, float), np.asarray(end, float)
    d = (end - start) / np.linalg.norm(end - start)
    shaft = Line3D(start, end - k * tip_h * d, thickness=k * thick, resolution=(1, 12))
    tip = Cone(direction=d, base_radius=k * tip_r, height=k * tip_h, resolution=(1, 16))
    tip.shift(end)
    v = VGroup(shaft, tip)
    v.set_fill(color, 1).set_stroke(color, 0.6)
    for m in v.get_family():
        m.shade_in_3d = False
    return v


def make_a():
    """a (BLUE) standing on the origin, with its label (s6's look)."""
    a = s6_vec3(P(A_VEC), BLUE)
    lbl = set_backstroke(MathTex(r"\mathbf a", font_size=46, color=BLUE), width=6)
    return a, lbl


GRID_STYLE = dict(color=FG, width=1.5, opacity=0.22)
S6_GRID = ((-3, 3), (-2, 7))      # s6's floor: whole s4 y in [-3, 3], whole s4 z in [-2, 7]
WIDE_GRID = ((-13, 7), (-6, 14))  # this scene's floor, faded in around it during {feed}


def make_floor():
    """s6's floor grid (the plane at right angles to a), and the rest of this scene's wider
    floor as separate segments in the same style, so nothing is drawn twice."""
    (y0, y1), (z0, z1) = S6_GRID
    (Y0, Y1), (Z0, Z1) = WIDE_GRID

    def seg(p, q):
        return Line(P(p), P(q))

    inner = VGroup(*[seg((0, y, z0), (0, y, z1)) for y in range(y0, y1 + 1)],
                   *[seg((0, y0, z), (0, y1, z)) for z in range(z0, z1 + 1)])
    outer = VGroup()
    for y in range(Y0, Y1 + 1):
        if y0 <= y <= y1:
            outer.add(seg((0, y, Z0), (0, y, z0)), seg((0, y, z1), (0, y, Z1)))
        else:
            outer.add(seg((0, y, Z0), (0, y, Z1)))
    for z in range(Z0, Z1 + 1):
        if z0 <= z <= z1:
            outer.add(seg((0, Y0, z), (0, y0, z)), seg((0, y1, z), (0, Y1, z)))
        else:
            outer.add(seg((0, Y0, z), (0, Y1, z)))
    for g in (inner, outer):
        g.set_stroke(GRID_STYLE["color"], GRID_STYLE["width"], opacity=GRID_STYLE["opacity"])
    return inner, outer


class Strip(VGroup):
    """project -> rotate 90 deg -> scale by |a|, fixed at the top."""

    def __init__(self):
        super().__init__()
        self.boxes, self.labels, self.ticks, self.arrows = VGroup(), VGroup(), VGroup(), VGroup()
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
            tick = check_mark(GREEN).scale(0.7).move_to(box.get_right() + 0.3 * LEFT)
            self.ticks.add(tick)          # not part of the strip until it is drawn
        for b1, b2 in zip(self.boxes[:-1], self.boxes[1:]):
            self.arrows.add(Arrow(b1.get_right(), b2.get_left(), buff=0.1, color=DIM,
                                  stroke_width=3, max_tip_length_to_length_ratio=0.35))
        self.add(self.boxes, self.labels, self.arrows)

    def light(self, i):
        return [self.boxes[i].animate.set_stroke(YELLOW, 3.5), self.labels[i].animate.set_color(YELLOW)]

    def tick(self, i):
        return [self.boxes[i].animate.set_stroke(GREEN, 3), self.labels[i].animate.set_color(FG),
                Create(self.ticks[i])]


def question_eq(size=46):
    """s6's question, split into pieces that can be born separately; the "?" is its own piece."""
    q = MathTex(r"\mathbf a\times(", r"\mathbf b+\mathbf c", r")", r"\overset{?}{=}",
                r"\mathbf a\times\mathbf b", r"+", r"\mathbf a\times", r"\mathbf c", font_size=size)
    q[1].set_color(GREEN)
    q[7].set_color(PINK)
    qm = max(q[3], key=lambda g: g.get_center()[1])        # the "?" sits above the "="
    qm.set_color(YELLOW)
    lhs = VGroup(*q[0], *q[1], *q[2])
    rel = VGroup(*[g for g in q[3] if g is not qm])
    rb, plus, rc = VGroup(*q[4]), VGroup(*q[5]), VGroup(*q[6], *q[7])
    return VGroup(lhs, rel, qm, rb, plus, rc), qm


# ── this scene's views (same angles throughout clips 1-2) ─────────────────────────────────────
PHI, THETA, FOCAL = 40 * DEGREES, 50 * DEGREES, 60
VIEW_A1 = dict(zoom=1.261, frame_center=(0.354, -0.357, 0.039))   # b, c, b + c and their shadows
VIEW_A2 = dict(zoom=1.261, frame_center=(-0.753, 0.572, 0.039))   # + the turned shadow
VIEW_B = dict(zoom=0.812, frame_center=(-3.66, 3.67, -0.38))      # the stretched picture
VIEW_C = dict(phi=60 * DEGREES, theta=40 * DEGREES, zoom=0.74,     # b's chain, t from -1 to 2
              frame_center=(-2.5, 2.0, 0.0))

B, C = np.array([1, 2, 0]), np.array([1, 1, 2])
BC = B + C
BS, CS, BCS = np.array([0, 2, 0]), np.array([0, 1, 2]), np.array([0, 3, 2])        # shadows
BR, CR, BCR = np.array([0, 0, 2]), np.array([0, -2, 1]), np.array([0, -2, 3])      # turned
BX, CX, BCX = 3 * BR, 3 * CR, 3 * BCR                                             # a x b, ...


def vec(v, color, start=(0, 0, 0), width=6, tip=0.3):
    s = P(start)
    e = P(np.add(start, v))
    return Arrow(s, e, buff=0, color=color, stroke_width=width, tip_length=tip,
                 max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=12)


def para_fill(u, v, op=0.1):
    return Polygon(P((0, 0, 0)), P(u), P(np.add(u, v)), P(v)).set_stroke(width=0).set_fill(FG, op)


def para_sides(u, v, dash=0.14, op=0.8):
    """Dashed far sides: a copy of v from u's tip (PINK) and of u from v's tip (YELLOW)."""
    s1 = DashedLine(P(u), P(np.add(u, v)), dash_length=dash).set_stroke(PINK, 3, op)
    s2 = DashedLine(P(v), P(np.add(u, v)), dash_length=dash).set_stroke(YELLOW, 3, op)
    return VGroup(s1, s2)


def born(src, dst):
    """TransformFromCopy between two texts, glyph for glyph (flat groups on both sides, so the
    target keeps its own glyphs: no new sub-objects that the 3D camera would not know are flat)."""
    return TransformFromCopy(VGroup(*src.family_members_with_points()),
                             VGroup(*dst.family_members_with_points()))


def tex(s, color=FG, size=44):
    return set_backstroke(MathTex(s, font_size=size, color=color), width=8)


class PanCamera(ThreeDCamera):
    """ThreeDCamera whose frame_center only pans the 3D projection.

    Stock CE also bakes frame_center into the 2D drawing matrix, once, at the first frame
    (a cached cairo context), which shifts every fixed-in-frame mobject by the opening
    frame_center and makes later pans inconsistent. Here the drawing matrix never shifts."""

    @property
    def frame_center(self):
        return ORIGIN

    @frame_center.setter
    def frame_center(self, point):
        self._frame_center.move_to(point)

    def project_points(self, points):
        fc = self._frame_center.get_center()
        fd, zoom = self.get_focal_distance(), self.get_zoom()
        points = np.dot(points - fc, self.get_rotation_matrix().T)
        zs = points[:, 2]
        factor = fd / (fd - zs)
        factor[(fd - zs) < 0] = 10**6
        points[:, 0] *= factor * zoom
        points[:, 1] *= factor * zoom
        return points


class NarratedScene(FlatNarratedScene, ThreeDScene):
    """The engine's NarratedScene with a 3D camera (vk finds scenes by `(NarratedScene)`)."""

    def __init__(self, **kwargs):
        kwargs.setdefault("camera_class", PanCamera)
        super().__init__(**kwargs)


class LinearSteps(NarratedScene):
    # ── helpers ───────────────────────────────────────────────────────────────────────────────
    def hud(self, *mobs):
        """Fix flat things to the frame (without adding them): the camera won't project them."""
        self.renderer.camera.add_fixed_in_frame_mobjects(*mobs)
        return mobs[0]

    def scr(self, p):
        """Where a scene point is on screen right now (frame coordinates)."""
        cam = self.renderer.camera
        cam.reset_rotation_matrix()            # the camera only refreshes it at capture time
        q = cam.project_point(np.asarray(p, dtype=float))
        return np.array([q[0], q[1], 0.0])

    def pin(self, lbl, p, off):
        """Put a flat label at a scene point, `off` away on screen; remembered for `track`."""
        lbl.p3, lbl.off = np.asarray(p, dtype=float), np.asarray(off, dtype=float)
        lbl.move_to(self.scr(lbl.p3) + lbl.off)
        return lbl

    def track(self, *lbls):
        for m in lbls:
            m.add_updater(lambda m: m.move_to(self.scr(m.p3) + m.off))

    def untrack(self, *lbls):
        for m in lbls:
            m.clear_updaters()

    def away(self, v, dist):
        """Screen offset from a vector's tip, continuing outward from the origin."""
        d = self.scr(P(v)) - self.scr(P((0, 0, 0)))
        return dist * d / np.linalg.norm(d)

    def cam_to(self, view, run_time, added=(), **kw):
        args = dict(phi=PHI, theta=THETA, focal_distance=FOCAL)
        args.update(view)
        args.update(kw)
        self.move_camera(**args, added_anims=list(added), run_time=run_time)

    # ── scene ─────────────────────────────────────────────────────────────────────────────────
    def construct(self):
        self.set_camera_orientation(**S6_CAM)
        self.floor_s6, self.floor_more = make_floor()
        self.floor_s6.set_z_index(-5)
        self.floor_more.set_z_index(-5)
        self.floor = VGroup(self.floor_s6, self.floor_more)
        self.a, self.a_lbl = make_a()
        self.a.set_z_index(3)
        self.strip = self.hud(Strip())
        self.hud(self.strip.ticks)
        self.hud(self.a_lbl)
        self.pin(self.a_lbl, P(A_VEC), A_LBL_OFF)

        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()

        self.play(*[FadeOut(m) for m in self.mobjects if isinstance(m, VMobject)],
                  run_time=1.0)   # end on an empty frame
        self.clear()
        self.wait(0.15)

    # ── c1.lin.1: b, c, b + c; project ────────────────────────────────────────────────────────
    def clip1(self):
        with self.say("c1.lin.1") as c:
            # s6 faded its last shot out: it fades back in, then the camera glides in
            self.play(FadeIn(self.floor_s6), FadeIn(self.a), FadeIn(self.strip), FadeIn(self.a_lbl),
                      run_time=0.6)
            self.track(self.a_lbl)
            machine = FlashAround(self.strip.boxes, color=YELLOW, time_width=1.5, buff=0.15)
            self.hud(machine.mobject)
            self.cam_to(VIEW_A1, run_time=min(1.6, 0.92 * c.until("bc")),
                        added=[machine, FadeIn(self.floor_more)])
            self.untrack(self.a_lbl)
            self.remove(self.floor_s6, self.floor_more)
            self.add(self.floor)
            c.wait_until("bc")

            self.b3, self.c3, self.bc3 = vec(B, YELLOW), vec(C, PINK), vec(BC, GREEN)
            for m in (self.b3, self.c3, self.bc3):
                m.set_z_index(1)
            self.lb = self.hud(tex(r"\mathbf b", YELLOW))
            self.lc = self.hud(tex(r"\mathbf c", PINK))
            self.lbc = self.hud(tex(r"\mathbf b+\mathbf c", GREEN))
            self.pin(self.lb, P(B), self.away(B, 0.42))
            self.pin(self.lc, P(C), self.away(C, 0.42))
            self.pin(self.lbc, P(BC), self.away(BC, 0.62))
            self.play(GrowArrow(self.b3), FadeIn(self.lb, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("vector see")
            self.play(GrowArrow(self.c3), FadeIn(self.lc, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("their sum")
            self.play(GrowArrow(self.bc3), FadeIn(self.lbc, shift=0.25 * DOWN), run_time=1.1)
            c.wait_until("parallelogram")
            self.sides3 = para_sides(B, C).set_z_index(0)
            self.fill3 = para_fill(B, C).set_z_index(-1)
            self.play(*[Create(s) for s in self.sides3], FadeIn(self.fill3), run_time=1.2)

            # {proj}: the light is straight above; every shadow drops, colours kept
            c.wait_until("proj")
            self.bs, self.cs, self.bcs = vec(BS, YELLOW), vec(CS, PINK), vec(BCS, GREEN)
            self.sides_s = para_sides(BS, CS)
            self.fill_s = para_fill(BS, CS, op=0.12)
            for m in (self.bs, self.cs, self.bcs, self.sides_s):
                m.set_z_index(-2)
            self.fill_s.set_z_index(-3)
            self.drops = VGroup(*[DashedLine(P(u), P(s), dash_length=0.1).set_stroke(DIM, 2.5)
                                  for u, s in ((B, BS), (C, CS), (BC, BCS))]).set_z_index(-1)
            self.play(TransformFromCopy(self.b3, self.bs), TransformFromCopy(self.c3, self.cs),
                      TransformFromCopy(self.bc3, self.bcs),
                      TransformFromCopy(self.sides3, self.sides_s),
                      TransformFromCopy(self.fill3, self.fill_s),
                      *[Create(d) for d in self.drops],
                      *[time_span(a, 0, 0.25) for a in self.strip.light(0)], run_time=2.0)
            self.floor_pic = VGroup(self.fill_s, self.sides_s, self.bs, self.cs, self.bcs)
            settle(self, self.floor_pic)

            # "the shadow of a parallelogram is a parallelogram": the 3D picture steps back
            c.wait_until("the shadow of a parallelogram")
            self.pic3 = VGroup(self.fill3, self.sides3, self.b3, self.c3, self.bc3)
            self.lab3 = VGroup(self.lb, self.lc, self.lbc)
            self.play(VGroup(self.sides3, self.b3, self.c3, self.bc3).animate.set_opacity(0.25),
                      self.fill3.animate.set_opacity(0), self.lab3.animate.set_opacity(0.4),
                      run_time=1.0)
            settle(self, self.pic3)
            settle(self, self.lab3)
            c.wait_until("is a parallelogram")
            outline = Polygon(P((0, 0, 0)), P(BS), P(BCS), P(CS)).set_stroke(FG, 6)
            self.play(VShowPassingFlash(outline, time_width=0.5), run_time=1.3)

            # {sum}: the GREEN shadow is the diagonal of the shadow parallelogram
            c.wait_until("sum")
            glow = Line(P((0, 0, 0)), P(BCS)).set_stroke(GREEN, 14)
            self.play(VShowPassingFlash(glow, time_width=0.7), run_time=1.4)
            c.wait_until("sum of the shadows")
            self.play(*self.strip.tick(0), run_time=0.8)

    # ── c1.lin.2: rotate, scale, read off ─────────────────────────────────────────────────────
    def clip2(self):
        with self.say("c1.lin.2") as c:
            # {rot}
            tracked = [self.a_lbl, *self.lab3]
            self.track(*tracked)
            self.cam_to(VIEW_A2, run_time=1.4,
                        added=[*self.strip.light(1), FadeOut(self.drops)])
            self.untrack(*tracked)
            c.wait_until("turn the whole")
            self.play(Rotate(self.floor_pic, angle=PI / 2, axis=OUT, about_point=ORIGIN),
                      run_time=2.5)
            c.wait_until("still a parallelogram")
            self.play(*self.strip.tick(1), run_time=0.8)

            # {stretch}: step back, then everything on the floor times |a| = 3
            c.wait_until("stretch")
            tracked = [self.a_lbl, *self.lab3]
            self.track(*tracked)
            self.cam_to(VIEW_B, run_time=1.3,
                        added=[*self.strip.light(2), FadeOut(self.pic3), FadeOut(self.lab3)])
            self.untrack(*tracked)
            self.bx, self.cx, self.bcx = vec(BX, YELLOW, tip=0.36), vec(CX, PINK, tip=0.36), \
                vec(BCX, GREEN, tip=0.36)
            for m in (self.bx, self.cx, self.bcx):
                m.set_z_index(-2)
            a_flash = Line(P((0, 0, 0)), P(A_VEC)).set_stroke(YELLOW, 12)
            self.play(Transform(self.bs, self.bx), Transform(self.cs, self.cx),
                      Transform(self.bcs, self.bcx),
                      self.fill_s.animate.scale(3, about_point=ORIGIN),
                      self.sides_s.animate.scale(3, about_point=ORIGIN),
                      time_span(VShowPassingFlash(a_flash, time_width=0.8), 0.1, 0.9), run_time=1.9)
            c.wait_until("still a parallelogram", nth=1)
            self.play(*self.strip.tick(2), run_time=0.8)

            # {read} ... {sides}
            c.wait_until("sides")
            self.lx_b = self.hud(tex(r"\mathbf a\times\mathbf b", YELLOW, 42))
            self.lx_c = self.hud(tex(r"\mathbf a\times\mathbf c", PINK, 42))
            self.pin(self.lx_b, P(BX / 2), 0.62 * LEFT + 0.42 * DOWN)
            self.pin(self.lx_c, P(CX / 2), 0.15 * LEFT + 0.55 * UP)
            self.play(LaggedStart(FadeIn(self.lx_b, shift=0.3 * DOWN),
                                  FadeIn(self.lx_c, shift=0.3 * DOWN), lag_ratio=0.5),
                      run_time=1.6)
            c.wait_until("diag")
            self.lx_bc = self.hud(tex(r"\mathbf a\times(\mathbf b+\mathbf c)", GREEN, 42))
            self.pin(self.lx_bc, P(0.62 * BCX), 0.25 * RIGHT + 0.55 * UP)
            glow = Line(P((0, 0, 0)), P(BCX)).set_stroke(GREEN, 14)
            self.play(FadeIn(self.lx_bc, shift=0.3 * DOWN), VShowPassingFlash(glow, time_width=0.6),
                      run_time=1.5)

            # {eq}: s6's question comes back, born from the three labels; the "?" drops out
            c.wait_until("eq")
            self.Q, qm = question_eq()
            self.Q.move_to(3.1 * DOWN)
            self.hud(self.Q)
            lhs, rel, _, rb, plus, rc = self.Q
            births = [born(self.lx_bc, lhs), born(self.lx_b, rb), born(self.lx_c, rc)]
            self.play(*births, FadeIn(rel), FadeIn(qm), FadeIn(plus), run_time=1.3)
            self.remove(*[b.mobject for b in births])
            settle(self, self.Q)
            c.wait_until("plus ay cross see")
            self.Q.remove(qm)
            self.qbox = self.hud(SurroundingRectangle(self.Q, color=GREEN, buff=0.2,
                                                      corner_radius=0.1).set_stroke(GREEN, 3))
            self.play(FadeOut(qm, shift=0.45 * DOWN), Create(self.qbox),
                      run_time=min(1.2, c.remaining))
            self.Qb = VGroup(self.Q, self.qbox)
            settle(self, self.Qb)

    # ── c1.lin.3: multiples too; linear ───────────────────────────────────────────────────────
    def clip3(self):
        with self.say("c1.lin.3") as c:
            # {scalar}: keep b's chain only
            gone = [self.cs, self.bcs, self.fill_s, self.sides_s, self.lx_c, self.lx_bc, self.lx_b]
            self.track(self.a_lbl)
            self.cam_to(VIEW_C, run_time=1.8,
                        added=[*[FadeOut(m) for m in gone],
                               self.Qb.animate.scale(0.82).move_to(3.6 * RIGHT + 1.45 * UP)])
            self.untrack(self.a_lbl)

            tt = self.tt = ValueTracker(1.0)

            def chain_arrow(v, color, width=6, z=0):
                def make():
                    t = tt.get_value()
                    if abs(t) < 0.04:
                        return VectorizedPoint(ORIGIN)
                    return vec(t * np.asarray(v), color, width=width, tip=0.36).set_z_index(z)
                return always_redraw(make)

            b_t = chain_arrow(B, YELLOW, z=1)
            s_t = chain_arrow(BS, YELLOW, width=5, z=-2)
            out_t = chain_arrow(BX, YELLOW, z=-2)
            drop_t = always_redraw(lambda: DashedLine(P(tt.get_value() * B), P(tt.get_value() * BS),
                                                      dash_length=0.1).set_stroke(DIM, 2.5)
                                   if abs(tt.get_value()) > 0.04 else VectorizedPoint(ORIGIN))
            self.remove(self.bs)          # the stretched b-arrow becomes the t = 1 output
            self.add(out_t)
            self.play(FadeIn(b_t), FadeIn(s_t), FadeIn(drop_t), run_time=0.8)

            # {t}: the GOLD slider
            c.wait_until("t")
            line = NumberLine(x_range=[-1, 2, 1], length=3.9, color=DIM, stroke_width=3,
                              include_numbers=True, font_size=32)
            line.numbers.set_color(DIM)
            line.move_to(3.15 * DOWN + 4.0 * LEFT)
            knob = Triangle(color=GOLD, fill_opacity=1).set_stroke(width=0).scale(0.14).rotate(PI)
            knob.add_updater(lambda m: m.next_to(line.n2p(tt.get_value()), UP, buff=0.06))
            readout = VGroup(MathTex("t=", font_size=40, color=GOLD),
                             DecimalNumber(1.0, num_decimal_places=1, font_size=40, color=GOLD))
            readout.arrange(RIGHT, buff=0.12)
            readout.add_updater(lambda m: (m[1].set_value(tt.get_value()), self.hud(m)))
            readout.next_to(line, UP, buff=0.5)
            self.slider = VGroup(line, knob, readout)
            self.hud(self.slider)
            knob.update()
            self.play(FadeIn(self.slider), run_time=0.8)
            self.play(tt.animate.set_value(2.0), run_time=2.0)
            c.wait_until("the same number")
            self.eq2 = MathTex(r"\mathbf a\times(", "t", r"\,\mathbf b)=", "t", r"\,(\mathbf a\times\mathbf b)",
                               font_size=46)
            self.eq2[1].set_color(GOLD)
            self.eq2[3].set_color(GOLD)
            self.eq2.scale(0.82).next_to(self.Qb, DOWN, buff=0.45)
            self.hud(self.eq2)
            self.play(FadeIn(self.eq2, shift=0.3 * UP), run_time=1.0)
            c.wait_until("flipping")
            self.play(tt.animate.set_value(-1.0), run_time=min(2.0, 0.85 * c.until("lin")))
            knob.clear_updaters()
            readout.clear_updaters()      # t has stopped: freeze the readout

            # {lin}
            c.wait_until("lin")
            self.lin = self.hud(T("linear", 46, YELLOW))
            self.lin_sub = self.hud(T("keeps sums and multiples", 30, FG))
            self.lin.next_to(self.eq2, DOWN, buff=0.6)
            self.lin_sub.next_to(self.lin, DOWN, buff=0.2)
            self.play(FadeIn(self.lin, shift=0.3 * DOWN), run_time=1.0)
            self.play(FadeIn(self.lin_sub, shift=0.2 * DOWN), run_time=0.8)

            # {chain}: one bracket under the three ticked boxes
            c.wait_until("chain")
            self.brace = self.hud(Brace(self.strip.boxes, DOWN, buff=0.12, color=YELLOW))
            self.chain_lbl = self.hud(T("linear", 34, YELLOW))
            self.chain_lbl.next_to(self.brace, DOWN, buff=0.1)
            self.play(GrowFromCenter(self.brace), TransformFromCopy(self.lin, self.chain_lbl),
                      run_time=1.5)
            self.chain = (b_t, s_t, out_t, drop_t)

    # ── c1.lin.4: the first slot, on a flat card ──────────────────────────────────────────────
    def clip4(self):
        with self.say("c1.lin.4") as c:
            for m in self.chain:
                m.clear_updaters()
            L1 = MathTex(r"(", r"\mathbf b+\mathbf c", r")\times\mathbf a", font_size=54)
            L1[1].set_color(GREEN)
            L2 = MathTex(r"=-\,\mathbf a\times(", r"\mathbf b+\mathbf c", r")", font_size=54)
            L2[1].set_color(GREEN)
            L3 = MathTex(r"=-\,\mathbf a\times\mathbf b-\mathbf a\times", r"\mathbf c", font_size=54)
            L3[1].set_color(PINK)
            L4 = MathTex(r"=\mathbf b\times\mathbf a+", r"\mathbf c", r"\times\mathbf a", font_size=54)
            L4[1].set_color(PINK)
            rows = [2.0, 1.0, 0.0, -1.0]
            L1.move_to(rows[0] * UP)
            for L, y in zip((L2, L3, L4), rows[1:]):
                L.move_to(y * UP)
                L.align_to(L1, LEFT).shift(0.9 * RIGHT)
            card = VGroup(L1, L2, L3, L4)
            tag2 = T("swap: minus sign", 30, DIM)
            tag4 = T("swap: minus sign", 30, DIM)
            tx = max(L2.get_right()[0], L3.get_right()[0], L4.get_right()[0]) + 0.7
            tag2.move_to(L2.get_center()).set_x(tx, direction=LEFT)
            tag4.move_to(L4.get_center()).set_x(tx, direction=LEFT)
            block = VGroup(card, tag2, tag4)
            block.shift(-block.get_center()[0] * RIGHT)
            self.hud(L1)            # born while the 3D camera is still on

            # {first}: the board clears; the first-slot version is born from the rule's left side
            keep = [self.Qb]
            gone = [m for m in self.mobjects if m not in keep and isinstance(m, VMobject)]
            c.wait_until("first slot")
            slot = FlashAround(self.Q[0][0], color=YELLOW, time_width=1.5, buff=0.08)
            self.hud(slot.mobject)
            self.play(slot, run_time=1.0)
            c.wait_until("borrow")
            birth = born(self.Q[0], L1)
            self.play(LaggedStart(*[FadeOut(m) for m in gone], lag_ratio=0.04),
                      self.Qb.animate.scale(1 / 0.82 * 0.9).move_to(3.15 * UP),
                      time_span(birth, 0.35, 1.4), run_time=1.4)
            for m in list(self.mobjects):
                if m not in keep:
                    self.remove(m)
            self.add(L1)
            # nothing 3D is left: back to the flat camera (fixed things look the same)
            self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1,
                                        focal_distance=20, frame_center=ORIGIN)

            # {borrow}: each line is born from the one above
            self.play(TransformMatchingStrings(L1.copy(), L2, run_time=1.4))
            c.wait_until("a minus sign")
            self.play(FadeIn(tag2, shift=0.2 * LEFT), run_time=0.8)
            c.wait_until("use the rule")
            fl = FlashAround(self.Qb, color=YELLOW, time_width=1.5, run_time=1.6)
            self.hud(fl.mobject)
            self.play(fl, TransformMatchingStrings(L2.copy(), L3, run_time=1.5))
            c.wait_until("swap back")
            self.play(TransformMatchingStrings(L3.copy(), L4, run_time=1.5))
            self.play(FadeIn(tag4, shift=0.2 * LEFT), run_time=0.7)

            # {result}
            c.wait_until("result")
            self.play(FlashAround(L1, color=GREEN, time_width=1.5), run_time=1.4)
            c.wait_until("is bee cross ay")
            self.rbox = SurroundingRectangle(L4, color=GREEN, buff=0.15, corner_radius=0.08)
            self.play(Create(self.rbox), run_time=1.0)

            c.wait_until("multiples come out")
            scal = MathTex(r"(t\,\mathbf b)\times\mathbf a=t\,(\mathbf b\times\mathbf a)",
                           font_size=42, color=DIM)
            scal.move_to(2.1 * DOWN).set_x(0)
            self.play(FadeIn(scal, shift=0.3 * UP), run_time=1.2)

            c.wait_until("conclude")
            concl = T("Multiply out brackets as usual, keeping the order.", 36, GREEN)
            concl.move_to(3.2 * DOWN)
            self.play(FadeIn(concl, shift=0.3 * UP), run_time=1.2)
        self.wait(1.8)          # let the upshot sit before the frame clears
