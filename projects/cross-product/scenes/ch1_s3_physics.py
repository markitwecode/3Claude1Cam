"""Chapter 1, scene 3: three laws (torque, angular momentum, magnetic force), one pattern. Clips c1.phys.1 – c1.phys.3.

Layout: the wrench is built big (hero) in clip 1, shrinks to the left panel at {spin}; the ball
fills the centre panel, the magnetic field the right one. At {strip} the physics fades, the three
arrow-triples take the same pose, then merge into one big a, b, a x b picture (handed to s4).
All pictures share one oblique projection: x right, y into the screen (up-right), z up.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── projection ─────────────────────────────────────────────────────────────────
TH = 72 * DEGREES                      # angle between a and b in the merged picture
TH_W = 60 * DEGREES                    # angle between r and F on the wrench
PSI = -30 * DEGREES                    # direction of a in the standard pose (towards the viewer)
EX = np.array([1.0, -0.2, 0.0])
EY = np.array([0.5, 0.5, 0.0])
EZ = np.array([0.0, 1.0, 0.0])
MAT = np.array([[EX[0], EY[0], 0.0], [EX[1], EY[1], 0.0], [0.0, 0.0, 1.0]])

M_TOP, M_SIDE, M_HEAD, M_EDGE = "#5d6676", "#3b414c", "#77819a", "#97a1b3"


def pv(x, y, z=0.0):
    return x * EX + y * EY + z * EZ


def flat(mob, o, z=0.0, s=1.0):
    """Map a mobject drawn in the xy plane (top view, centred on ORIGIN) into the view."""
    mob.scale(s, about_point=ORIGIN)
    mob.apply_matrix(MAT, about_point=ORIGIN)
    mob.shift(np.array(o, dtype=float) + s * z * EZ)
    return mob


def _hull(pts):
    P = sorted({(round(p[0], 6), round(p[1], 6)) for p in pts})

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in P:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(P):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return [np.array([x, y, 0.0]) for x, y in lower[:-1] + upper[:-1]]


def prism(poly, o, z_top, z_bot, s, top_col):
    """A convex prism: silhouette (dark sides, outlined) and its top face."""
    top = [o + s * pv(x, y, z_top) for x, y in poly]
    bot = [o + s * pv(x, y, z_bot) for x, y in poly]
    sil = Polygon(*_hull(top + bot)).set_fill(M_SIDE, 1).set_stroke(M_EDGE, 1.5)
    face = Polygon(*top).set_fill(top_col, 1).set_stroke(width=0)
    return sil, face


def circle_pts(r, n=64):
    return [(r * np.cos(t), r * np.sin(t)) for t in np.linspace(0, TAU, n, endpoint=False)]


def vec(a, b, color, width=6, tip=0.28):
    return Arrow(a, b, buff=0, stroke_width=width, tip_length=tip, color=color,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=30)


def right_angle(o, d1, d2, u, color, width=3):
    return VMobject().set_points_as_corners(
        [o + u * d1, o + u * (d1 + d2), o + u * d2]).set_stroke(color, width)


def tex(s, size, color=FG):
    return MathTex(s, font_size=size, color=color)


def unit(v):
    return v / np.linalg.norm(v)


class Wrench:
    """Bolt + wrench with r, F, tau. Built big (s=1) and again as the small panel."""

    def __init__(self, o, s=1.0, lsize=48, off=1.0, sw=6, tip=0.3):
        o = np.array(o, dtype=float)
        self.o, self.s = o, s

        def P(x, y, z=0.0):
            return o + s * pv(x, y, z)

        shaft_sil, _ = prism(circle_pts(0.28), o, -0.14, -1.7, s, M_SIDE)
        threads = VGroup(*[
            VMobject().set_points_smoothly(
                [P(0.28 * np.cos(t), 0.28 * np.sin(t), z0 + 0.08 * (t - PI) / PI)
                 for t in np.linspace(PI, TAU, 12)]).set_stroke(M_EDGE, 1.5)
            for z0 in np.arange(-0.5, -1.65, -0.17)])
        ring_sil, ring_top = prism(circle_pts(0.8), o, 0.0, -0.14, s, M_TOP)
        hpts = [(0.5, -0.27), (5.4, -0.27), (5.4, 0.27), (0.5, 0.27)]
        hand_sil, hand_top = prism(hpts, o, 0.0, -0.14, s, M_TOP)
        hexp = [(0.46 * np.cos(k * PI / 3 + PI / 6), 0.46 * np.sin(k * PI / 3 + PI / 6))
                for k in range(6)]
        head_sil, head_top = prism(hexp, o, 0.22, 0.0, s, M_HEAD)
        self.body = VGroup(shaft_sil, threads, ring_sil, hand_sil, ring_top, hand_top,
                           head_sil, head_top)

        hz = 0.15                                   # the plane the arrows float in
        self.H = H = P(4.4, 0, hz)                  # the hand
        fx, fy = 2.6 * np.cos(TH_W), 2.6 * np.sin(TH_W)
        Fend = H + s * pv(fx, fy)
        self.r = vec(P(0, 0, hz), H, BLUE, sw, tip)
        self.F = vec(H, Fend, YELLOW, sw, tip)
        self.tau = vec(P(0, 0, 0.22), P(0, 0, 2.9), TEAL, sw, tip)

        turn = Arc(radius=0.62, start_angle=-40 * DEGREES, angle=280 * DEGREES,
                   color=FG, stroke_width=4)
        turn.add_tip(tip_length=0.26, tip_width=0.26)
        self.turn = flat(turn, o, z=1.0, s=s).set_stroke(opacity=0.85)

        self.lr = tex(r"\mathbf r", lsize, BLUE).next_to(P(2.2, -0.27, -0.14), DOWN,
                                                         buff=0.16 * off)
        self.lF = tex(r"\mathbf F", lsize, YELLOW).move_to(
            Fend + unit(Fend - H) * 0.42 * off + UP * 0.06)
        self.ltau = tex(r"\boldsymbol\tau", lsize, TEAL).next_to(self.tau.get_end(), LEFT,
                                                                buff=0.22 * off)

        # the decomposition and the angle (big view only)
        self.Fpar = vec(H, H + s * pv(fx, 0), DIM, sw, tip)
        self.Fperp = vec(H, H + s * pv(0, fy), YELLOW, sw, tip)
        self.guides = VGroup(
            DashedLine(self.Fpar.get_end(), Fend, dash_length=0.08),
            DashedLine(self.Fperp.get_end(), Fend, dash_length=0.08)).set_stroke(DIM, 2)
        self.rt = right_angle(H, s * pv(1, 0), s * pv(0, 1), 0.3, YELLOW)
        self.th_arc = flat(Arc(radius=0.8, start_angle=0, angle=TH_W, color=FG, stroke_width=3),
                           o + s * pv(4.4, 0), z=hz, s=s)
        self.lth = tex(r"\theta", lsize - 4).move_to(
            H + s * pv(1.3 * np.cos(TH_W / 2), 1.3 * np.sin(TH_W / 2)))
        self.rt_tau = right_angle(P(0, 0, 0.22), s * pv(1, 0), s * pv(0, 0, 1), 0.32, TEAL)


def dir_a():
    return np.array([np.cos(PSI), np.sin(PSI)])


def dir_b():
    return np.array([np.cos(PSI + TH), np.sin(PSI + TH)])


def triple(o, la, lb, lc, sw, tip):
    """The standard pose: a towards the viewer-right, b at TH from it, a x b up."""
    o = np.array(o, dtype=float)
    return (vec(o, o + pv(*(la * dir_a())), BLUE, sw, tip),
            vec(o, o + pv(*(lb * dir_b())), YELLOW, sw, tip),
            vec(o, o + pv(0, 0, lc), TEAL, sw, tip))


def cross_formula(prod, left, right, size, pre=None):
    """prod = left x right, coloured TEAL / BLUE / YELLOW (with an optional scalar)."""
    parts = [prod, "=", *([pre] if pre else []), left, r"\times", right]
    f = MathTex(*parts, font_size=size, color=FG)
    f[0].set_color(TEAL)
    f[-3].set_color(BLUE)
    f[-1].set_color(YELLOW)
    return f


O_BIG = np.array([-4.1, -0.4, 0.0])          # bolt, big view
O_PAN = np.array([-6.07, -0.2, 0.0])          # bolt, left panel
S_PAN = 0.5
C_BALL = np.array([-0.2, -0.3, 0.0])         # centre of the circle
R_BALL, P_LEN, PHI0 = 1.35, 1.1, -10 * DEGREES
Q = np.array([4.3, -0.2, 0.0])               # the charge
V_LEN, F_LEN = 1.45, 1.6
PANEL_X = (-4.6, 0.0, 4.45)
FORM_Y = -2.45
OB = np.array([-3.3, -0.2, 0.0])              # the merged a, b picture


class Physics(NarratedScene):
    def construct(self):
        # ── handoff from s2 ────────────────────────────────────────────────────
        axb = tex(r"\mathbf a\times\mathbf b", 72, TEAL)
        self.play(FadeIn(axb), run_time=0.5)
        self.wait(0.2)

        W = Wrench(O_BIG)
        strength = MathTex(r"|\mathbf r|", r"\,|\mathbf F|", r"\,\sin", r"\theta",
                           font_size=60, color=GOLD).move_to([4.9, 2.0, 0])
        torque = cross_formula(r"\boldsymbol\tau", r"\mathbf r", r"\mathbf F", 60)
        torque.move_to([4.9, 0.8, 0])

        with self.say("c1.phys.1") as c:
            self.play(time_span(FadeOut(axb), 0, 0.8),
                      FadeIn(W.body, lag_ratio=0.1, run_time=1.8), run_time=1.8)
            c.wait_until("at some distance")
            self.play(GrowArrow(W.r), FadeIn(W.lr, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("with some force")
            self.play(GrowArrow(W.F), FadeIn(W.lF, shift=0.3 * DOWN), run_time=1.1)

            c.wait_until("part")
            self.play(ReplacementTransform(W.F.copy(), W.Fpar),
                      ReplacementTransform(W.F.copy(), W.Fperp),
                      W.F.animate.set_opacity(0.35), run_time=1.8)
            self.play(Create(W.guides), Create(W.rt), run_time=0.8)
            c.wait_until("turns it")
            self.play(Create(W.turn), run_time=min(1.2, max(0.6, c.until("strength"))))

            c.wait_until("the distance")
            self.play(TransformFromCopy(W.lr, strength[0]),
                      TransformFromCopy(W.lF, strength[1]), run_time=1.3)
            c.wait_until("the sine of the angle")
            self.play(Create(W.th_arc), FadeIn(W.lth), run_time=0.7)
            self.play(FadeIn(strength[2]), TransformFromCopy(W.lth, strength[3]), run_time=1.0)
            settle(self, strength)

            c.wait_until("axis")
            self.play(GrowArrow(W.tau), run_time=1.5)
            c.wait_until("at right angles to both")
            self.play(Create(W.rt_tau), run_time=0.8)

            c.wait_until("torque")
            self.play(FadeIn(VGroup(torque[0], torque[1], torque[3]), shift=0.3 * DOWN),
                      TransformFromCopy(W.lr, torque[2]),
                      TransformFromCopy(W.lF, torque[4]),
                      FadeIn(W.ltau, shift=0.3 * DOWN), run_time=1.4)
            settle(self, torque)

        # ── ball on a string, then the charge in a field ───────────────────────
        Wp = Wrench(O_PAN, s=S_PAN, lsize=36, off=0.7, sw=5, tip=0.2)
        torque_p = torque.copy().scale(44 / 60).move_to([PANEL_X[0], FORM_Y, 0])

        phi = ValueTracker(PHI0 - TAU)

        def bpos():
            a = phi.get_value()
            return C_BALL + pv(R_BALL * np.cos(a), R_BALL * np.sin(a))

        path = DashedVMobject(flat(Circle(radius=R_BALL), C_BALL), num_dashes=48)
        path.set_stroke(DIM, 2.5)
        centre = Dot(C_BALL, radius=0.06, color=FG)
        string = always_redraw(lambda: Line(C_BALL, bpos(), stroke_width=2.5, color=FG))
        ball = always_redraw(lambda: Dot(bpos(), radius=0.14, color=FG))

        b0 = C_BALL + pv(R_BALL * np.cos(PHI0), R_BALL * np.sin(PHI0))
        pdir = pv(-np.sin(PHI0), np.cos(PHI0))
        r_b = vec(C_BALL, b0 - unit(b0 - C_BALL) * 0.15, BLUE, 5, 0.2)
        p_b = vec(b0 + unit(pdir) * 0.15, b0 + P_LEN * pdir, YELLOW, 5, 0.2)
        L_b = vec(C_BALL, C_BALL + pv(0, 0, 1.9), TEAL, 5, 0.2)
        lr_b = tex(r"\mathbf r", 36, BLUE).move_to((C_BALL + b0) / 2 + UP * 0.3)
        lp_b = tex(r"\mathbf p", 36, YELLOW).next_to(p_b.get_end(), RIGHT, buff=0.12)
        lL_b = tex(r"\mathbf L", 36, TEAL).next_to(L_b.get_end(), LEFT, buff=0.18)
        formL = cross_formula(r"\mathbf L", r"\mathbf r", r"\mathbf p", 44)
        formL.move_to([PANEL_X[1], FORM_Y, 0])

        alpha = ValueTracker(70 * DEGREES)

        def v_end():
            a = alpha.get_value()
            return Q + V_LEN * pv(np.sin(a), np.cos(a))

        def v_lbl_pos():
            d = unit(v_end() - Q)
            return (Q + v_end()) / 2 + np.array([d[1], -d[0], 0]) * 0.36

        field_xz = [(-1.2, 1.0), (-1.2, -0.9), (1.5, 1.15), (1.5, -0.9)]
        field = VGroup(*[vec(Q + pv(x, -1.15, z), Q + pv(x, 1.15, z), YELLOW, 4, 0.2)
                         for x, z in field_xz])
        lB = tex(r"\mathbf B", 36, YELLOW).next_to(field[0].get_end(), UL, buff=0.06)
        charge = Dot(Q, radius=0.13, color=FG)
        lq = tex("q", 36).next_to(charge, DL, buff=0.08)
        v = vec(Q, v_end(), BLUE, 5, 0.2)
        lv = tex(r"\mathbf v", 36, BLUE).move_to(v_lbl_pos())
        Fm = vec(Q, Q + pv(0, 0, F_LEN * np.sin(alpha.get_value())), TEAL, 5, 0.2)
        lFm = tex(r"\mathbf F", 36, TEAL).next_to(Fm.get_end(), RIGHT, buff=0.15)
        formF = cross_formula(r"\mathbf F", r"\mathbf v", r"\mathbf B", 44, pre="q\\,")
        formF.move_to([PANEL_X[2], FORM_Y, 0])
        zero = tex("0", 48, GOLD).move_to(Q + UP * 0.75)

        with self.say("c1.phys.2") as c:
            fades = [W.Fpar, W.Fperp, W.guides, W.rt, W.th_arc, W.lth, W.rt_tau, strength]
            keys = ("body", "r", "F", "tau", "turn", "lr", "lF", "ltau")
            self.play(*[time_span(FadeOut(m), 0, 0.6) for m in fades],
                      *[time_span(ReplacementTransform(getattr(W, k), getattr(Wp, k)), 0.2, 1.4)
                        for k in keys],
                      time_span(Transform(torque, torque_p), 0.2, 1.4),
                      *[time_span(FadeIn(m), 0.8, 1.6) for m in (path, centre, string, ball)],
                      run_time=1.6)
            self.play(phi.animate.set_value(PHI0), run_time=1.8, rate_func=smooth)
            string.clear_updaters()
            ball.clear_updaters()

            c.wait_until("the position cross the momentum")
            self.play(GrowArrow(r_b), GrowArrow(p_b), FadeIn(lr_b), FadeIn(lp_b), run_time=1.2)
            c.wait_until("points along the axis")
            self.play(GrowArrow(L_b), FadeIn(lL_b, shift=0.2 * DOWN),
                      time_span(FadeIn(formL, shift=0.3 * DOWN), 0.5, 1.6), run_time=1.6)

            c.wait_until("magnet")
            self.play(FadeIn(charge), FadeIn(lq), GrowArrow(v), FadeIn(lv), run_time=1.0)
            c.wait_until("a magnetic field")
            self.play(LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=0.15),
                      FadeIn(lB), run_time=1.3)
            c.wait_until("feels a force")
            self.play(GrowArrow(Fm), FadeIn(lFm, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("its velocity and the field")
            self.play(FadeIn(formF, shift=0.3 * DOWN), run_time=1.0)

            c.wait_until("along")

            def upd_F(m):
                ln = F_LEN * np.sin(alpha.get_value())
                m.become(vec(Q, Q + pv(0, 0, max(ln, 0.02)), TEAL, 5, 0.2))
                m.set_opacity(min(1.0, ln / 0.25))

            v.add_updater(lambda m: m.become(vec(Q, v_end(), BLUE, 5, 0.2)))
            lv.add_updater(lambda m: m.move_to(v_lbl_pos()))
            Fm.add_updater(upd_F)
            self.play(time_span(alpha.animate.set_value(0), 0, 1.4),
                      time_span(FadeOut(lFm), 0, 0.7),
                      time_span(FadeIn(zero, scale=0.6), 1.0, 1.6), run_time=1.6)
            for m in (v, lv, Fm):
                m.clear_updaters()
            self.remove(Fm)

        # ── strip the physics: one pattern ─────────────────────────────────────
        std = [triple([x - 0.92, -0.3, 0], 2.0, 1.7, 1.6, 5, 0.22) for x in PANEL_X]
        A, B, Cb = triple(OB, 4.5, 3.8, 3.0, 7, 0.32)
        a_mid = (A.get_start() + A.get_end()) / 2
        a_dir = unit(A.get_end() - A.get_start())
        la = tex(r"\mathbf a", 52, BLUE).move_to(a_mid + np.array([-a_dir[1], a_dir[0], 0]) * -0.45)
        lb = tex(r"\mathbf b", 52, YELLOW).move_to(B.get_end() + unit(B.get_end() - OB) * 0.45)
        th_arc = flat(Arc(radius=1.0, start_angle=PSI, angle=TH, color=FG, stroke_width=3), OB)
        lth = tex(r"\theta", 48).move_to(
            OB + pv(1.5 * np.cos(PSI + TH / 2), 1.5 * np.sin(PSI + TH / 2)))
        size = MathTex(r"|\mathbf a|", r"\,|\mathbf b|", r"\,\sin", r"\theta",
                       font_size=60, color=GOLD).move_to([4.3, 0.5, 0])
        laxb = tex(r"\mathbf a\times\mathbf b", 52, TEAL).next_to(Cb.get_end(), LEFT, buff=0.25)
        ra1 = right_angle(OB, pv(*dir_a()), pv(0, 0, 1), 0.4, TEAL)
        ra2 = right_angle(OB, pv(*dir_b()), pv(0, 0, 1), 0.4, TEAL)
        defn = T("That pattern is the definition.", size=44, color=YELLOW).move_to([0, -3.2, 0])

        with self.say("c1.phys.3") as c:
            gone = [Wp.body, Wp.turn, Wp.lr, Wp.lF, Wp.ltau, path, centre, string, ball,
                    lr_b, lp_b, lL_b, charge, lq, lv, lB, field[0], field[2], field[3]]
            moves = [ReplacementTransform(Wp.r, std[0][0]), ReplacementTransform(Wp.F, std[0][1]),
                     ReplacementTransform(Wp.tau, std[0][2]),
                     ReplacementTransform(r_b, std[1][0]), ReplacementTransform(p_b, std[1][1]),
                     ReplacementTransform(L_b, std[1][2]),
                     ReplacementTransform(v, std[2][0]), ReplacementTransform(field[1], std[2][1])]
            self.play(*[time_span(FadeOut(m), 0, 1.0) for m in gone],
                      time_span(FadeOut(zero), 1.0, 1.8),
                      *[time_span(m, 0.6, 2.0) for m in moves],
                      time_span(GrowArrow(std[2][2]), 1.0, 2.0), run_time=2.0)

            c.wait_until("two")
            extra = [A.copy(), A.copy(), B.copy(), B.copy()]
            self.play(ReplacementTransform(std[0][0], A), ReplacementTransform(std[1][0], extra[0]),
                      ReplacementTransform(std[2][0], extra[1]),
                      ReplacementTransform(std[0][1], B), ReplacementTransform(std[1][1], extra[2]),
                      ReplacementTransform(std[2][1], extra[3]),
                      *[time_span(FadeOut(m), 0, 0.8)
                        for m in (std[0][2], std[1][2], std[2][2], torque, formL, formF)],
                      time_span(FadeIn(la, shift=0.2 * DOWN), 1.0, 1.6),
                      time_span(FadeIn(lb, shift=0.2 * DOWN), 1.0, 1.6),
                      time_span(Create(th_arc), 1.0, 1.6), time_span(FadeIn(lth), 1.1, 1.6),
                      run_time=1.6)
            self.remove(*extra)

            c.wait_until("the two lengths")
            self.play(TransformFromCopy(la, size[0]), TransformFromCopy(lb, size[1]), run_time=1.3)
            c.wait_until("the sine of the angle")
            self.play(FadeIn(size[2]), TransformFromCopy(lth, size[3]), run_time=1.0)
            settle(self, size)

            c.wait_until("dir")
            self.play(GrowArrow(Cb), FadeIn(laxb, shift=0.3 * DOWN), run_time=1.4)
            c.wait_until("at right angles to both")
            self.play(Create(ra1), Create(ra2), run_time=0.8)
            c.wait_until("defn")
            self.play(FadeIn(defn, shift=0.3 * UP), run_time=1.0)

        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects if not isinstance(m, ValueTracker)],
                  run_time=1.0)
        self.wait(0.15)
