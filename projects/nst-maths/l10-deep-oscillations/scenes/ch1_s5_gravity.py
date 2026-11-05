"""Chapter 1, scene 5: what pulls a pendulum back (gravity split along rod and swing). Clips c1.gravity.1 – c1.gravity.4.

Shared helpers (load_scene("ch1_s5_gravity")):
  pendulum(theta=30, labels=True, angle=True)  the pendulum drawing (hatched ceiling, DIM dashed
      vertical, FG rod "L", BLUE bob "m", YELLOW θ at the pivot); θ in degrees, + = bob left.
      .ceil .hatch .pin .vert .rod .bob .m_label .L_label .arc .theta_label .B (bob centre)
  gravity_split(theta=30, label=True)  gravity's arrow mg (FG) and its two parts head to tail:
      .weight (B→W), .along (DIM, along the rod outward, mg cos θ), .swing (RED, along the swing,
      mg sin θ, toward the bottom), .corner (DIM right-angle mark), .weight_label ("mg").
  split_labels(theta)  .along_label (DIM mg cos θ), .swing_label (RED mg sin θ).
  force_formula()  F = -mg sin θ (F RED, θ YELLOW); [2] is the minus.
  opening_shot()  s4's last frame (legend with k, m, ω + corner tag).
  handover_shot()  this scene's last frame (s6 opens on it).
"""
# style: 2
# handover: next
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

# ── pendulum geometry (inside kit.PICTURE) ──────────────────────────────────────
PIVOT = np.array([-3.2, 2.7, 0])
ROD_L = 2.75
BOB_R = 0.28
G_LEN = 1.5            # length of the mg arrow

# legend entries
E_X_SHORT = (r"x", BLUE, "displacement")
E_M = ("m", FG, "mass")
E_L = ("L", FG, "rod length")
E_TH = (r"\theta", YELLOW, "angle (radians)")
E_G = ("g", FG, r"9.81 m/s²")
LEG_ROWS = 4
FINAL_ENTRIES = [E_X_SHORT, kit.E_XD, kit.E_XDD, E_M, E_L, E_TH, E_G]


def _dirs(theta):
    th = theta * DEGREES
    u = np.array([-np.sin(th), -np.cos(th), 0.0])     # along the rod, outward (pivot → bob)
    t = np.array([np.cos(th), -np.sin(th), 0.0])      # along the swing (toward the bottom for θ > 0)
    return u, t


def bob_center(theta, pivot=PIVOT, length=ROD_L):
    return pivot + length * _dirs(theta)[0]


def pendulum(theta=30, labels=True, angle=True, pivot=PIVOT, length=ROD_L):
    """The pendulum drawing at angle theta (degrees; positive = bob left of the vertical)."""
    u, t = _dirs(theta)
    P = np.array(pivot, dtype=float)
    B = P + length * u
    ceil = Line(P + LEFT * 0.85, P + RIGHT * 0.85).set_stroke(FG, 4)
    hatch = VGroup(*[Line(P + RIGHT * x, P + RIGHT * (x + 0.2) + UP * 0.2).set_stroke(FG, 2)
                     for x in np.linspace(-0.8, 0.6, 8)])
    vert = DashedLine(P, P + DOWN * (length + 0.45), dash_length=0.1).set_stroke(DIM, 2.5)
    rod = Line(P, B).set_stroke(FG, 4)
    pin = Dot(P, radius=0.06, color=FG)
    bob = Circle(radius=BOB_R).set_fill(BLUE, 1).set_stroke(BLUE, 2).move_to(B).set_z_index(3)
    g = VGroup(ceil, hatch, vert, rod, pin, bob)
    g.ceil, g.hatch, g.vert, g.rod, g.pin, g.bob, g.B = ceil, hatch, vert, rod, pin, bob, B
    g.arc = g.theta_label = g.m_label = g.L_label = None
    if angle:
        th = theta * DEGREES
        op = min(1.0, abs(theta) / 10.0)
        arc = Arc(radius=0.7, start_angle=-PI / 2, angle=-th if abs(th) > 1e-3 else -1e-3,
                  arc_center=P).set_stroke(YELLOW, 4, opacity=op)
        a = -PI / 2 - th / 2
        lab = MathTex(r"\theta", font_size=34, color=YELLOW)
        lab.move_to(P + 1.02 * np.array([np.cos(a), np.sin(a), 0])).set_opacity(op)
        g.add(arc, lab)
        g.arc, g.theta_label = arc, lab
    if labels:
        L = MathTex("L", font_size=34).move_to(P + 1.75 * u + 0.32 * t)
        m = MathTex("m", font_size=32, color=BG).move_to(B).set_z_index(4)
        g.add(L, m)
        g.L_label, g.m_label = L, m
    return g


def _arrow(a, b, color, width=5):
    if np.linalg.norm(b - a) < 0.03:
        return VMobject()
    return Arrow(a, b, buff=0, stroke_width=width, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, color=color).set_z_index(1)


def gravity_split(theta=30, label=True, pivot=PIVOT, length=ROD_L, G=G_LEN):
    """Gravity's arrow at the bob and its two parts, head to tail (a right-angled triangle with
    mg as hypotenuse): along the rod outward (DIM), along the swing toward the bottom (RED)."""
    u, t = _dirs(theta)
    B = np.array(pivot, dtype=float) + length * u
    th = theta * DEGREES
    W = B + G * DOWN
    C = B + G * np.cos(th) * u
    weight = _arrow(B, W, FG)
    along = _arrow(B, C, DIM)
    swing = _arrow(C, W, RED)
    sw = W - C
    n = np.linalg.norm(sw)
    if n > 0.05:
        w = sw / n
        s = min(0.16, 0.4 * n)
        corner = VMobject().set_points_as_corners([C - s * u, C - s * u + s * w, C + s * w])
        corner.set_stroke(DIM, 2)
    else:
        corner = VMobject()
    g = VGroup(weight, along, swing, corner)
    g.weight, g.along, g.swing, g.corner = weight, along, swing, corner
    g.B, g.C, g.W = B, C, W
    g.weight_label = None
    if label:
        lab = MathTex("mg", font_size=32).move_to(B + np.array([0.42 * np.clip((theta + 3.0) / 3.0, -1, 1), -0.8, 0]))
        g.add(lab)
        g.weight_label = lab
    return g


def split_labels(theta=30, pivot=PIVOT, length=ROD_L, G=G_LEN):
    u, t = _dirs(theta)
    B = np.array(pivot, dtype=float) + length * u
    th = theta * DEGREES
    W = B + G * DOWN
    C = B + G * np.cos(th) * u
    al = MathTex(r"mg\cos\theta", font_size=30, color=DIM).move_to((B + C) / 2 - 0.62 * t)
    sl = MathTex(r"mg\sin\theta", font_size=30, color=RED).move_to((C + W) / 2 + 0.42 * u)
    g = VGroup(al, sl)
    g.along_label, g.swing_label = al, sl
    return g


def force_formula(size=kit.COL_SIZE):
    f = MathTex("F", "=", "-", "m", "g", r"\sin", r"\theta", font_size=size)
    f[0].set_color(RED)
    f[6].set_color(YELLOW)
    return f


def opening_shot():
    """s4's last frame = this scene's first."""
    return kit.chrome([kit.E_X, kit.E_XD, kit.E_XDD, ("k", FG, "stiffness"), ("m", FG, "mass"),
                       (r"\omega", FG, "pull back per unit stretch, per kg")])


def handover_shot():
    """This scene's last frame = s6's first: pendulum frozen at 30° with gravity split,
    F = -mg sin θ at the top of the column, the legend (max_rows 4) and the corner tag.
    .pend .split .force .legend .tag"""
    pend = pendulum(30)
    split = gravity_split(30)
    force = kit.col_place(force_formula(), 0)
    leg = kit.legend(FINAL_ENTRIES, LEG_ROWS)
    tag_ = kit.corner_tag()
    g = VGroup(pend, split, force, leg, tag_)
    g.pend, g.split, g.force, g.legend, g.tag = pend, split, force, leg, tag_
    return g


def _num_after(m, label, base_glyph):
    """A live readout number right of `label`, its baseline on `base_glyph`'s bottom."""
    m.next_to(label, RIGHT, buff=0.18)
    return m.align_to(base_glyph, DOWN)


def _col_line(tex_parts, i, colors=None):
    m = MathTex(*tex_parts, font_size=kit.COL_SIZE)
    for k, col in (colors or {}).items():
        m[k].set_color(col)
    return kit.col_place(m, i)


class Gravity(NarratedScene):
    def construct(self):
        op = opening_shot()
        self.add(*op)
        leg = op.legend
        leg.max_rows = LEG_ROWS

        P = pendulum(30)
        S = gravity_split(30)
        SL = split_labels(30)
        u, t = _dirs(30)
        B = P.B

        # extras around the bob
        rodpull = _arrow(B - 0.42 * u - 0.2 * t, B - 1.35 * u - 0.2 * t, DIM, width=4)
        tangent = DashedLine(B - 1.7 * t, B + 1.7 * t, dash_length=0.12).set_stroke(DIM, 2.5)
        s = 0.42
        ra_mark = VMobject().set_points_as_corners([B - s * u, B - s * u + s * t, B + s * t])
        ra_mark.set_stroke(DIM, 2)
        qmark = MathTex("?", font_size=48, color=YELLOW).move_to(
            B + 0.9 * np.array([np.cos(110 * DEGREES), np.sin(110 * DEGREES), 0]))
        notes_tag = kit.tag("the notes call this angle x(t) · scan p. 10", P.theta_label, RIGHT, buff=0.55)
        ext = DashedLine(B, B + 1.75 * u, dash_length=0.1).set_stroke(DIM, 2.5)
        th30 = 30 * DEGREES
        arc_b = Arc(radius=0.55, start_angle=-PI / 2, angle=-th30, arc_center=B).set_stroke(YELLOW, 4)
        a = -PI / 2 - th30 / 2
        th_b = MathTex(r"\theta", font_size=30, color=YELLOW).move_to(B + 0.95 * np.array([np.cos(a), np.sin(a), 0]))

        card = kit.move_card("Split gravity along the rod and the swing: only the swing part drives.")

        # column: lines 1..5 (line 0 is kept free under the move card)
        l1 = _col_line([r"\angle(mg,\ \text{vertical})", "=", "0"], 1)
        s1 = kit.step_label("gravity: straight down", 1)[1]
        l2 = _col_line([r"\angle(\text{rod},\ \text{vertical})", "=", r"\theta"], 2, {2: YELLOW})
        s2 = kit.step_label("the rod leans off the vertical", 2)[1]
        l3 = _col_line([r"\angle(mg,\ \text{rod})", "=", r"\theta"], 3, {2: YELLOW})
        s3 = kit.step_label("so gravity is that angle off the rod", 3)
        l4 = _col_line([r"\text{swing part}", "=", "m", "g", r"\sin", r"\theta"], 4, {0: RED, 5: YELLOW})
        s4 = kit.step_label("opposite side = hypotenuse × sine", 4)
        F = kit.col_place(force_formula(), 5)
        s5 = kit.step_label("points back to the bottom", 5)

        tri = kit.triangle_card(small=True)
        tri.move_to([3.8, -2.75, 0])

        # ── clip 1: the pendulum and its two forces ──
        with self.say("c1.gravity.1") as c:
            self.play(*appear(P.ceil, P.hatch, P.pin, shift=None), run_time=1.0)
            c.wait_until("called the bob")
            kit.legend_set(self, leg, [E_X_SHORT, kit.E_XD, kit.E_XDD, E_M],
                           Create(P.rod), FadeIn(P.bob, scale=0.6), run_time=min(1.2, c.until("of length L")))
            c.wait_until("of length L")
            kit.legend_add(self, leg, E_L, extra=appear(P.L_label))
            c.wait_until("from the vertical")
            self.play(Create(P.vert), run_time=min(1.2, c.until("call it theta")))
            c.wait_until("call it theta")
            kit.legend_add(self, leg, E_TH, extra=[Create(P.arc), *appear(P.theta_label, notes_tag, lag=0.4)])  # early: notes tag rides with θ
            c.wait_until("Gravity pulls")
            self.play(GrowArrow(S.weight), run_time=min(1.5, c.until("the mass M")))
            c.wait_until("the mass M")
            self.play(*appear(P.m_label, shift=None), run_time=0.8)
            c.wait_until("times G")
            kit.legend_add(self, leg, E_G, extra=appear(S.weight_label))
            c.wait_until("And the rod pulls")
            self.play(GrowArrow(rodpull), *disappear(notes_tag), run_time=min(1.5, c.until("toward the pivot") + 0.8))
            c.wait_until("can only move")
            self.play(Create(tangent), run_time=min(1.5, c.until("at right angles")))
            c.wait_until("at right angles")
            self.play(Create(ra_mark), run_time=1.0)
            c.wait_until("So the rod can't")
            self.play(FlashAround(rodpull, color=DIM, time_width=1.5), run_time=1.5)

        # ── clip 2: which part of gravity? the move, then the angle between them ──
        with self.say("c1.gravity.2") as c:
            self.play(*appear(qmark), run_time=1.0)
            c.wait_until("split gravity")
            self.play(*appear(card, shift=None), run_time=1.0)
            c.wait_until("Only the part")
            self.play(VShowPassingFlash(tangent.copy().set_stroke(YELLOW, 6), time_width=0.6), run_time=1.5)
            c.wait_until("Gravity points")
            self.play(*appear(s1, l1, lag=0.3, shift=None), FlashAround(S.weight, time_width=1.5),
                      run_time=min(1.5, c.until("The rod leans")))
            c.wait_until("The rod leans")
            self.play(*appear(s2, l2, lag=0.3, shift=None), run_time=min(1.5, c.until("So gravity and")))  # early: the label is read with its sentence ("leans … the vertical")
            c.wait_until("So gravity and")
            self.play(Create(ext), TransformFromCopy(P.arc, arc_b), run_time=1.5)
            self.play(*appear(th_b, shift=None), *appear(s3, l3, lag=0.3, shift=None), run_time=1.2)

        # ── clip 3: split gravity; read off the swing part; the sign ──
        with self.say("c1.gravity.3") as c:
            self.play(*disappear(qmark), FlashAround(S.weight, time_width=1.5), run_time=1.2)
            c.wait_until("one side along the rod")
            self.play(ReplacementTransform(S.weight.copy(), S.along), *appear(SL.along_label),
                      run_time=1.5)
            c.wait_until("one along the swing")
            self.play(ReplacementTransform(S.weight.copy(), S.swing), Create(S.corner), run_time=1.5)
            c.wait_until("opposite")
            self.play(*appear(tri), run_time=1.0)
            c.wait_until("M times G")
            self.play(*appear(SL.swing_label, s4, l4, lag=0.3, shift=None), *set_alpha([l1, s1], 0.4),
                      run_time=1.5)
            c.wait_until("just like the triangle")
            self.play(FlashAround(tri.formula, time_width=1.5), run_time=1.5)
            c.wait_until("It points back")
            self.play(VShowPassingFlash(S.swing.copy().set_stroke(YELLOW, 8), time_width=0.8),
                      run_time=1.2)
            c.wait_until("so the pull is")
            self.play(*during(disappear(tri), 0, 0.4), *during(appear(s5, F, lag=0.3, shift=None), 0.4, 1),
                      *set_alpha([l2, s2], 0.4), run_time=1.6)
            c.wait_until("minus M times G")
            self.play(FlashAround(F[2], time_width=1.5), run_time=min(1.5, c.until(floor=0.8)))

        # ── clip 4: the live sweep ──
        th = ValueTracker(30)
        r1 = MathTex(r"\theta =", font_size=34, color=YELLOW)
        kit.col_place(r1, 6.2)
        r2 = MathTex(r"\text{pull} = mg\,\times", font_size=34, color=RED)
        kit.col_place(r2, 7.0)

        def _row1():
            v = th.get_value()
            d, r = round(v), v * DEGREES
            m = T(f"{d:.0f}° = {r:.2f} rad".replace("-", "−"), size=26, color=YELLOW)
            return _num_after(m, r1, r1[0][0])

        def _row2():
            v = th.get_value()
            m = T(f"{abs(np.sin(v * DEGREES)):.3f}", size=26, color=RED)
            return _num_after(m, r2, r2[0][1])

        v1, v2 = _row1(), _row2()
        readouts = VGroup(r1, v1, r2, v2)

        with self.say("c1.gravity.4") as c:
            clutter = [tangent, ra_mark, rodpull, ext, arc_b, th_b, SL.along_label, SL.swing_label]
            self.play(*during(disappear(*clutter), 0, 0.5), *during(appear(readouts, shift=None), 0.5, 1),
                      run_time=1.6)
            # swap the static drawing for live ones
            self.remove(*P.get_family(), *S.get_family())
            pend_r = always_redraw(lambda: pendulum(th.get_value()))
            split_r = always_redraw(lambda: gravity_split(th.get_value()))
            v1r, v2r = always_redraw(_row1), always_redraw(_row2)
            self.remove(*v1.get_family(), *v2.get_family())
            self.add(pend_r, split_r, v1r, v2r)

            c.wait_until("At the bottom")
            self.play(th.animate.set_value(0), run_time=min(2.5, c.until("no pull")))
            c.wait_until("Swing out to forty")
            self.play(th.animate.set_value(40), run_time=min(4.0, c.until("sixty-four percent")))
            c.wait_until("Swing to the other side")
            self.play(th.animate.set_value(-40), run_time=min(4.2, c.until("Read it back") - 0.2),
                      rate_func=linear)
            c.wait_until("Read it back")
            self.play(th.animate.set_value(30), run_time=min(2.5, c.until("the further out")))
            th.set_value(30)
            self.remove(pend_r, split_r, v1r, v2r)
            P2, S2, v1, v2 = pendulum(30), gravity_split(30), _row1(), _row2()
            self.add(P2, S2, v1, v2)
            readouts = VGroup(r1, v1, r2, v2)
            c.wait_until("not by the angle")
            self.play(FlashAround(VGroup(F[5], F[6]), time_width=1.5), run_time=1.5)

        # ── handover: keep the picture, F to the top of the column ──
        self.play(*during(disappear(card, l1, s1, l2, s2, l3, s3, l4, s4, s5, readouts), 0, 0.5),
                  *during([F.animate.move_to(kit.col_point(0), aligned_edge=LEFT)], 0.4, 1),
                  run_time=1.8)
        self.wait(1.0)
