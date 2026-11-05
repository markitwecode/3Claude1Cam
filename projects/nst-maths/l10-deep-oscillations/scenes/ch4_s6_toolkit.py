"""Chapter 4, scene 6: the toolkit (three rules, integrating, the fan, the circuit). Clips c4.tools.1 – c4.tools.3.

Also exports the toolkit's PICTURES (load_scene("ch4_s6_toolkit")), for s7's recap and a later
impedance video. Every `t`, `gap`, `back` is a ValueTracker (the picture redraws every frame) or a
plain number (a still picture). Each picture is VGroup(static, dynamic) with .static (the plane,
DIM, built once), .dynamic (arrows, shadows: redrawn from the plane's *current* place and size),
.op (ValueTracker 0..1, the dynamic part's opacity), .plane. So you can move or scale `.static`
alone (`pic.static.animate.scale(0.5).move_to(p)`) and the arrows follow, still turning.
Fade in: `self.add(pic.dynamic)` with `pic.op.set_value(0)`, then play `show(pic)`.
  W_D = 1.3 display turning rate (so iωA is 1.3 long and -ω²A 1.69: true lengths, all fit).
  panel_commute(t, scale=PANEL_SCALE, origin=ORIGIN, omega=W_D)
      rule 1: GOLD arrow, GREEN velocity at its tip, BLUE shadow dot with a GREEN velocity tick on
      the axis; the GREEN arrow's shadow (dashed drop) lands exactly on the tick's end.
  panel_cancel(t, gap=0.0, scale=PANEL_SCALE, origin=ORIGIN, omega=W_D)
      rule 2: solid GOLD A1 = 0.95 and dashed GOLD A2 = 0.95 + 0.6i·gap, turning together; BLUE dot
      (A1's shadow) and BLUE ring (A2's). Shadows agree only while the gap points vertically;
      gap → 0 slides A2 onto A1 and the shadows agree at every t.
  panel_quarter(t, back=0.0, scale=PANEL_SCALE, origin=ORIGIN, omega=W_D, label=True)
      rule 3: GOLD arrow, GREEN iω×it at its tip, right-angle mark, GREEN "× iω" (static .label).
      back 0 → 1: the GREEN arrow turns a quarter back, shrinks by ω and slides onto the GOLD (÷ iω).
  fan(t, scale=FAN_SCALE, origin=ORIGIN, omega=W_D, tracks=True)
      GOLD A, GREEN iωA, RED -ω²A from the origin, a quarter turn apart, tip labels, right-angle
      mark; coloured shadow dots on Re; three readout tracks under the plane (labels x, ẋ, ẍ
      on their right) with a dot each at its arrow's shadow.
  circuit_small(scale=1.0, arrows=True)  the notes' series circuit (source V with ~, R, C, current
      I), still, centred at ORIGIN; inside the loop V, I, V_R, V_C each with a small FG frozen arrow.
      .labels (4 VGroups) .wires .source .resistor .capacitor
  panel_title(k), panel_caption(k) (k = 1, 2, 3), fan_caption(), show(pic), hide(pic).
"""
# style: 2
import math
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
ak = load_scene("ch2_s3_velocity")
hook = load_scene("ch4_s1_hook")

# ═══════════════════════════════ the toolkit pictures (shared) ═══════════════════════════════
W_D = 1.3
PANEL_SCALE = 0.45            # unit circle radius 0.585
FAN_SCALE = 0.615             # unit circle radius 0.8
PHI1, PHI2, PHI3, PHI_F = 0.4, 0.0, 0.9, 0.6


def _v(x):
    return x.get_value() if hasattr(x, "get_value") else float(x)


def _live(*xs):
    return any(hasattr(x, "get_value") for x in xs)


def _geo(static):
    """Origin and kit scale read off the static plane's unit circle (where it is now)."""
    c = static.plane.circle
    return c.get_center(), c.width / (2 * ak.PLANE_R)


def _fade(g, op):
    if op >= 0.999:
        return g
    for m in g.family_members_with_points():
        m.set_stroke(opacity=m.get_stroke_opacity() * op, family=False)
        m.set_fill(opacity=m.get_fill_opacity() * op, family=False)
    return g


def _picture(static, build, *params):
    op = ValueTracker(1.0)

    def b():
        o, s = _geo(static)
        return _fade(build(o, s), op.get_value())

    dyn = always_redraw(b) if _live(*params) else b()
    pic = VGroup(static, dyn)
    pic.static, pic.dynamic, pic.op, pic.plane = static, dyn, op, static.plane
    return pic


def show(pic):
    """Fade a picture in (its dynamic part must already be added with op 0)."""
    return [FadeIn(pic.static), pic.op.animate.set_value(1.0)]


def hide(pic):
    return [FadeOut(pic.static), pic.op.animate.set_value(0.0)]


def _static_plane(scale, origin, re_units=1.5, im_units=1.5):
    pl = ak.plane(scale, origin, re_units, im_units, labels=False)
    st = VGroup(pl)
    st.plane = pl
    return st


def _drop(tip, foot, color=DIM, width=2):
    if np.linalg.norm(tip - foot) > 0.05:
        return DashedLine(tip, foot, dash_length=0.07).set_stroke(color, width)
    return Line(tip, foot).set_stroke(color, width, opacity=0)


def _dashed_arrow(start, end, color, width=4):
    a = ak.arrow_between(start, end, color, width, z=-1.9)
    shaft = DashedLine(start, a.tip.get_base(), dash_length=0.08).set_stroke(color, width)
    shaft.set_z_index(-1.9)
    tip = a.tip.copy().set_z_index(-1.9)
    return VGroup(shaft, tip)


def panel_commute(t, scale=PANEL_SCALE, origin=ORIGIN, omega=W_D):
    st = _static_plane(scale, origin)

    def build(o, s):
        tv = _v(t)
        p = ak.phasor(tv, omega, PHI1)
        v = 1j * omega * p
        gold = ak.turning_arrow(tv, omega, PHI1, 1.0, GOLD, s, o, width=5)
        green = ak.velocity_arrow(tv, 1.0, omega, PHI1, 1.0, GREEN, s, o, width=5)
        tip_v = ak.plane_point(p + v, s, o)
        foot_x = ak.plane_point(p.real, s, o)
        foot_v = ak.plane_point((p + v).real, s, o)
        sh = ak.shadow(tv, omega, PHI1, 1.0, s, o)
        gdrop = _drop(tip_v, foot_v, GREEN, 2).set_opacity(0.7)
        if np.linalg.norm(foot_v - foot_x) > 0.14:
            tick = ak.arrow_between(foot_x, foot_v, GREEN, 6, z=-1.65)
        else:
            tick = Line(foot_x, foot_v).set_stroke(GREEN, 6).set_z_index(-1.65)
        sh.dot.set_z_index(-1.6)
        return VGroup(gold, green, sh.line, gdrop, tick, sh.dot)

    return _picture(st, build, t)


def panel_cancel(t, gap=0.0, scale=PANEL_SCALE, origin=ORIGIN, omega=W_D):
    st = _static_plane(scale, origin)

    def build(o, s):
        tv, g = _v(t), _v(gap)
        rot = complex(math.cos(omega * tv + PHI2), math.sin(omega * tv + PHI2))
        a1, a2 = 0.95 * rot, (0.95 + 0.6j * g) * rot
        p1, p2 = ak.plane_point(a1, s, o), ak.plane_point(a2, s, o)
        f1, f2 = ak.plane_point(a1.real, s, o), ak.plane_point(a2.real, s, o)
        solid = ak.arrow_between(o, p1, GOLD, 5)
        dashed = _dashed_arrow(o, p2, GOLD, 4)
        d1, d2 = _drop(p1, f1), _drop(p2, f2)
        dot = Dot(f1, radius=0.08, color=BLUE).set_z_index(-1.6)
        ring = Circle(radius=0.13 * s / PANEL_SCALE).move_to(f2).set_stroke(BLUE, 2.5)
        ring.set_z_index(-1.6)
        return VGroup(solid, dashed, d1, d2, dot, ring)

    return _picture(st, build, t, gap)


def quarter_label(pic):
    """The GREEN "× iω" by panel 3's plane (upper right)."""
    o, s = _geo(pic.static)
    u = ak.PLANE_R * s
    lab = MathTex(r"\times", "i", r"\omega", font_size=34 * s / PANEL_SCALE, color=GREEN)
    lab[1].set_color(PINK)
    lab.move_to(o + np.array([1.75 * u + 0.42 * s / PANEL_SCALE, 0.75 * u, 0]))
    return lab


def panel_quarter(t, back=0.0, scale=PANEL_SCALE, origin=ORIGIN, omega=W_D, label=True):
    st = _static_plane(scale, origin)

    def build(o, s):
        tv, b = _v(t), _v(back)
        p = ak.phasor(tv, omega, PHI3)
        gold = ak.turning_arrow(tv, omega, PHI3, 1.0, GOLD, s, o, width=5)
        if b < 0.005:
            green = ak.velocity_arrow(tv, 1.0, omega, PHI3, 1.0, GREEN, s, o, width=5)
            mark = ak.right_angle(tv, True, omega, PHI3, 1.0, 0.2, s, o)
            return VGroup(gold, green, mark)
        k = 1 - b
        vec = p * (omega ** k) * complex(math.cos(PI / 2 * k), math.sin(PI / 2 * k))
        start = ak.plane_point(k * p, s, o)
        end = ak.plane_point(k * p + vec, s, o)
        green = ak.arrow_between(start, end, GREEN, 5, z=-1.8)
        return VGroup(gold, green)

    pic = _picture(st, build, t, back)
    pic.label = None
    if label:
        pic.label = quarter_label(pic)
        st.add(pic.label)
    return pic


FAN_TIPS = ((r"A", GOLD), (r"i\omega A", GREEN), (r"-\omega^2 A", RED))


def fan(t, scale=FAN_SCALE, origin=ORIGIN, omega=W_D, tracks=True):
    st = _static_plane(scale, origin, re_units=2.0, im_units=1.5)
    o0 = np.array(origin, dtype=float)
    u0 = ak.PLANE_R * scale
    k_s = scale / FAN_SCALE
    st.tracks, st.track_labels = VGroup(), VGroup()
    if tracks:
        for k, (tex, col) in enumerate(((r"x", BLUE), (r"\dot{x}", GREEN), (r"\ddot{x}", RED))):
            y = o0[1] - 1.75 * u0 - (0.55 + 0.28 * k) * k_s
            ln = Line(o0 + [-2.0 * u0, 0, 0], o0 + [2.0 * u0, 0, 0]).set_y(y).set_stroke(DIM, 2)
            lab = MathTex(tex, font_size=30 * k_s, color=col).next_to(ln, RIGHT, buff=0.2 * k_s)
            st.tracks.add(ln)
            st.track_labels.add(lab)
        st.add(st.tracks, st.track_labels)
    tip_tex = [MathTex(tx, font_size=30 * k_s, color=c) for tx, c in FAN_TIPS]
    tip_tex[1][0][0].set_color(PINK)
    cols = (GOLD, GREEN, RED)

    def build(o, s):
        tv = _v(t)
        p = ak.phasor(tv, omega, PHI_F)
        amps = (p, 1j * omega * p, -omega ** 2 * p)
        u = ak.PLANE_R * s
        r = s / FAN_SCALE
        out = VGroup()
        arrows = [ak.turning_arrow(tv, omega, PHI_F, 1.0, GOLD, s, o, width=5),
                  ak.velocity_arrow(tv, 0.0, omega, PHI_F, 1.0, GREEN, s, o, width=5),
                  ak.accel_arrow(tv, 0.0, omega, PHI_F, 1.0, RED, s, o, width=5)]
        out.add(*arrows)
        out.add(ak.right_angle(tv, False, omega, PHI_F, 1.0, 0.2, s, o))
        for z, col, tx in zip(amps, cols, tip_tex):
            tip = ak.plane_point(z, s, o)
            foot = ak.plane_point(z.real, s, o)
            out.add(_drop(tip, foot))
            out.add(Dot(foot, radius=0.075 * r, color=col).set_z_index(-1.6))
            d = np.array([z.real, z.imag, 0.0]) / abs(z)
            lab = tx.copy().scale(s / scale)
            half = 0.5 * math.hypot(lab.width * abs(d[0]), lab.height * abs(d[1])) + 0.5 * lab.height
            lab.move_to(tip + d * (0.12 * r + half))
            out.add(lab)
        if len(st.tracks):
            for z, col, ln in zip(amps, cols, st.tracks):
                out.add(Dot([o[0] + z.real * u, ln.get_center()[1], 0], radius=0.075 * r,
                            color=col).set_z_index(-1.6))
        return out

    pic = _picture(st, build, t)
    return pic


def circuit_small(scale=1.0, arrows=True):
    W, H = 3.4, 2.6
    x0, x1, y0, y1 = -W / 2, W / 2, -H / 2, H / 2
    src_r = 0.32
    wires = VGroup(
        Line([x0, y1, 0], [x0, src_r, 0]), Line([x0, -src_r, 0], [x0, y0, 0]),
        Line([x0, y1, 0], [-0.5, y1, 0]), Line([0.5, y1, 0], [x1, y1, 0]),
        Line([x1, y1, 0], [x1, 0.1, 0]), Line([x1, -0.1, 0], [x1, y0, 0]),
        Line([x1, y0, 0], [x0, y0, 0]),
    ).set_stroke(FG, 3)
    ring = Circle(radius=src_r).move_to([x0, 0, 0]).set_stroke(FG, 3)
    sim = MathTex(r"\sim", font_size=40, color=FG).move_to([x0, 0, 0])
    source = VGroup(ring, sim)
    zz = [[-0.5, y1, 0]] + [[-0.5 + 0.0625 + 0.125 * k, y1 + (0.16 if k % 2 == 0 else -0.16), 0]
                            for k in range(8)] + [[0.5, y1, 0]]
    resistor = VMobject().set_points_as_corners(zz).set_stroke(FG, 3)
    capacitor = VGroup(Line([x1 - 0.3, 0.1, 0], [x1 + 0.3, 0.1, 0]),
                       Line([x1 - 0.3, -0.1, 0], [x1 + 0.3, -0.1, 0])).set_stroke(FG, 4)
    cur = Arrow([0.35, y0, 0], [-0.35, y0, 0], buff=0, stroke_width=4, tip_length=0.2,
                max_tip_length_to_length_ratio=0.4, color=FG)
    r_lab = MathTex("R", font_size=32, color=FG).next_to(resistor, UP, buff=0.12)
    c_lab = MathTex("C", font_size=32, color=FG).next_to(capacitor, RIGHT, buff=0.12)

    def tagged(tex, angle, pos):
        lab = MathTex(tex, font_size=32, color=FG)
        g = VGroup(lab)
        if arrows:
            d = np.array([math.cos(angle), math.sin(angle), 0])
            a = Arrow(ORIGIN, 0.42 * d, buff=0, stroke_width=4, tip_length=0.14,
                      max_tip_length_to_length_ratio=0.4, color=FG)
            a.next_to(lab, RIGHT, buff=0.12)
            g.add(a)
        g.move_to(pos)
        return g

    labels = VGroup(tagged("V", 0.0, [x0 + 0.85, 0, 0]),
                    tagged("I", 35 * DEGREES, [0, y0 + 0.45, 0]),
                    tagged("V_R", 35 * DEGREES, [0, y1 - 0.5, 0]),
                    tagged("V_C", -55 * DEGREES, [x1 - 0.9, 0, 0]))
    g = VGroup(wires, source, resistor, capacitor, cur, r_lab, c_lab, labels)
    g.wires, g.source, g.resistor, g.capacitor, g.current = wires, source, resistor, capacitor, cur
    g.component_labels, g.labels = VGroup(r_lab, c_lab), labels
    g.drawing = VGroup(wires, source, resistor, capacitor, cur, r_lab, c_lab)
    if abs(scale - 1) > 1e-6:
        g.scale(scale, about_point=ORIGIN)
    return g


def panel_title(k):
    """The panel's short rule name (FG, d/dt GREEN, e^{iωt} GOLD, i PINK)."""
    if k == 1:
        m = MathTex(r"\mathrm{Re}\text{ and }", r"d/dt", r"\text{ commute}", font_size=32)
        m[1].set_color(GREEN)
    elif k == 2:
        m = MathTex(r"e^{i\omega t}", r"\text{ cancels}", font_size=32)
        m[0].set_color(GOLD)
    else:
        m = MathTex(r"d/dt", r"\text{ is }", r"\times", "i", r"\omega", font_size=32)
        m[0].set_color(GREEN)
        m[3].set_color(PINK)
    return m


def panel_caption(k, size=30):
    if k == 1:
        m = MathTex(r"\frac{d}{dt}", r"\,\mathrm{Re}\big[", r"A\,e^{i\omega t}", r"\big]", "=",
                    r"\mathrm{Re}\bigg[", r"\frac{d}{dt}", r"\,A\,e^{i\omega t}", r"\bigg]",
                    font_size=size)
        for i in (0, 6):
            m[i].set_color(GREEN)
        for i in (2, 7):
            m[i].set_color(GOLD)
        m.left_side, m.right_side = VGroup(*m[0:4]), VGroup(*m[5:9])
        return m
    if k == 2:
        a = MathTex(r"\mathrm{Re}\big[", r"A_1 e^{i\omega t}", r"\big]", "=", r"\mathrm{Re}\big[",
                    r"A_2 e^{i\omega t}", r"\big]", font_size=size)
        b = MathTex(r"\text{for every } t", r"\;\Rightarrow\;", r"A_1 = A_2", font_size=size)
        a[1].set_color(GOLD)
        a[5].set_color(GOLD)
        b[2].set_color(GOLD)
        m = VGroup(a, b).arrange(DOWN, buff=0.16)
        m.top, m.bottom = a, b
        return m
    m = MathTex(r"\big(", r"e^{i\omega t}", r"\big)'", "=", "i", r"\omega", r"\,e^{i\omega t}",
                font_size=size)
    m[1].set_color(GOLD)
    m[6].set_color(GOLD)
    m[4].set_color(PINK)
    return m


def fan_caption(size=34):
    m = MathTex(r"\text{one }", r"e^{i\omega t}", r"\text{, a frozen arrow each}", font_size=size)
    m[1].set_color(GOLD)
    return m


# ═══════════════════════════════ the scene ═══════════════════════════════
PANEL_XS = (-4.45, 0.0, 4.45)
PANEL_Y = 0.4
TITLE_Y = -0.86
CAP_Y = -1.48
ROW_Y = 2.5
ROW_XS = (-5.75, -4.45, -3.15)
FAN_O = np.array([0.6, -0.35, 0])
FAN_O2 = np.array([3.95, -0.35, 0])
CIRCUIT_C = np.array([-4.15, -0.2, 0])
BAND_X = -1.6
ROW_BAND_Y, TAG_BAND_Y, EX_X = -2.55, -3.2, 3.15

E_A = (r"A", GOLD, "complex amplitude")
E_W = (r"\omega", FG, "turning rate")
E_A12 = (r"A_1,\ A_2", GOLD, "two complex amplitudes")


def _hl_box(m):
    b = RoundedRectangle(corner_radius=0.08, width=m.width + 0.32, height=m.height + 0.22)
    b.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.14).move_to(m).set_z_index(-1)
    return b


class Toolkit(NarratedScene):
    def construct(self):
        t = ValueTracker(0.0)
        ak.clock(t)
        self.add(t)
        self.gap_t = ValueTracker(1.0)
        self.back_t = ValueTracker(0.0)
        self.t = t
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c4.tools.1: the three rules ────────────────────────────────────────────
    def clip1(self):
        t = self.t
        p1 = panel_commute(t, origin=[PANEL_XS[0], PANEL_Y, 0])
        p2 = panel_cancel(t, self.gap_t, origin=[PANEL_XS[1], PANEL_Y, 0])
        p3 = panel_quarter(t, self.back_t, origin=[PANEL_XS[2], PANEL_Y, 0], label=False)
        self.pics = (p1, p2, p3)
        titles = [panel_title(k).move_to([x, TITLE_Y, 0]) for k, x in zip((1, 2, 3), PANEL_XS)]
        caps = [panel_caption(k, 28 if k == 2 else 30) for k in (1, 2, 3)]
        for c, x in zip(caps, PANEL_XS):
            if c.width > 4.15:
                c.scale_to_fit_width(4.15)
            c.move_to([x, CAP_Y, 0])
        caps[1].move_to([PANEL_XS[1], CAP_Y - 0.1, 0])
        self.titles, self.caps = titles, caps
        notes = kit.tag("the lecturer's three rules · notes p. 110, handwritten")
        notes.move_to([-kit.EDGE_X, 2.05, 0], aligned_edge=UL)
        self.notes = notes
        pin = hook.amp_pin()
        corner = kit.corner_tag("reference")
        leg = kit.legend([E_A, E_W])
        self.leg = leg
        for p in self.pics:
            p.op.set_value(0.0)
            self.add(p.dynamic)

        with self.say("c4.tools.1") as c:
            ak.run(t, True)
            self.play(*appear(pin, corner, leg, shift=None, lag=0.15), run_time=1.0)  # early: chrome of the scene
            anims = appear(*[p.static for p in self.pics], *titles, notes, shift=None, lag=0.12)
            for k, p in enumerate(self.pics):
                anims += during(p.op.animate.set_value(1.0), 0.1 * k, 0.4 + 0.1 * k)
            self.play(*anims, run_time=min(2.4, c.until("move")))  # early: the toolkit shown whole, then walked
            c.wait_until("move")
            card = kit.move_card("Make every oscillating quantity a frozen arrow: "
                                 "calculus becomes multiplication.")
            self.card = card
            self.play(*appear(card, shift=None), run_time=1.0)  # early: the move card shown whole as "the move here" is said
            c.wait_until("r1")
            box = _hl_box(titles[0])
            self.box = box
            self.play(FadeIn(box), *appear(caps[0], shift=None), run_time=1.5)
            c.wait_until("The velocity of the shadow")
            self.play(FlashUnder(caps[0].left_side, color=GREEN, run_time=1.4, time_width=1.5))
            c.wait_until("shadow of the velocity")
            self.play(FlashUnder(caps[0].right_side, color=GREEN, run_time=1.4, time_width=1.5))
            c.wait_until("r2")
            kit.legend_add(self, leg, E_A12, run_time=1.2,
                           extra=[Transform(box, _hl_box(titles[1]))])
            c.wait_until("are the same arrow")
            self.play(self.gap_t.animate.set_value(0.0), run_time=min(2.0, c.until("So you can cancel")))
            c.wait_until("So you can cancel")
            self.play(*appear(caps[1].top, caps[1].bottom, shift=None, lag=0.3), run_time=1.5)
            c.wait_until("r3")
            self.play(Transform(box, _hl_box(titles[2])), run_time=1.0)
            c.wait_until("multiplies")
            lab = quarter_label(p3)
            self.qlab = lab
            self.play(*appear(lab, caps[2], lag=0.3), run_time=1.5)

    # ── c4.tools.2: integrating runs the other way ──────────────────────────────
    def clip2(self):
        p3 = self.pics[2]
        integ = MathTex(r"\int", r"A\,e^{i\omega t}", r"\,dt", "=", r"\frac{A}{i\omega}",
                        r"\,e^{i\omega t}", font_size=34)
        integ[1].set_color(GOLD)
        integ[5].set_color(GOLD)
        integ[4][0].set_color(GOLD)
        integ[4][2].set_color(PINK)
        integ.move_to([BAND_X, ROW_BAND_Y, 0], aligned_edge=LEFT)
        const = kit.tag("+ a constant: 0 for a pure swing").move_to([BAND_X, TAG_BAND_Y, 0], aligned_edge=LEFT)
        ask = MathTex(r"\int", r"\;?", font_size=40, color=YELLOW).move_to(integ[0:3])
        div = MathTex(r"\div", "i", r"\omega", font_size=34, color=GREEN)
        div[1].set_color(PINK)
        div.move_to(self.qlab)
        ex = MathTex(r"\frac{12 + 9i}{3i}", "=", r"3 - 4i", font_size=34)
        ex[0][0:5].set_color(GREEN)
        ex[2].set_color(GOLD)
        ex.move_to([EX_X, ROW_BAND_Y, 0], aligned_edge=LEFT)
        extag = kit.tag("velocity → position").move_to([EX_X, TAG_BAND_Y, 0], aligned_edge=LEFT)
        self.band = [integ, const, ex[0], ex[1], ex[2], extag]

        with self.say("c4.tools.2") as c:
            self.play(*appear(ask), run_time=1.0)
            c.wait_until("integrate")
            self.play(self.back_t.animate.set_value(1.0), *swap(self.qlab, div),
                      run_time=min(2.0, c.until("It divides")))
            self.qlab = div
            c.wait_until("It divides")
            self.play(*swap(ask, integ), run_time=1.2)
            c.wait_until("up to a constant")
            self.play(*appear(const), run_time=1.0)
            c.wait_until("example")
            self.play(*appear(ex[0], ex[1], ex[2], extag, shift=None, lag=0.3), run_time=1.6)
            c.wait_until("three minus four")
            self.play(FlashAround(ex[2], color=GOLD, run_time=1.4, time_width=1.5))

    # ── c4.tools.3: the fan, then the circuit ───────────────────────────────────
    def clip3(self):
        t = self.t
        fn = fan(t, origin=FAN_O)
        fn.op.set_value(0.0)
        cap = fan_caption(32).move_to([FAN_O[0], -3.27, 0])
        circ = circuit_small().move_to(CIRCUIT_C)
        alg = MathTex(r"\text{calculus}", r"\;\to\;", r"\text{algebra}", font_size=38, color=YELLOW)
        alg.move_to([-0.1, 1.2, 0])

        with self.say("c4.tools.3") as c:
            leaving = [*self.titles, *self.caps, self.box, self.notes, self.qlab, *self.band]
            moves = [p.static.animate.scale(0.5).move_to([x, ROW_Y, 0])
                     for p, x in zip(self.pics, ROW_XS)]
            self.play(*during(disappear(*leaving), 0, 0.45), *during(moves, 0.3, 1.0),
                      *during(self.back_t.animate.set_value(0.0), 0.3, 1.0), run_time=1.8)
            self.add(fn.dynamic)
            self.play(*show(fn), run_time=1.2)
            c.wait_until("all turning")
            self.play(*appear(cap), run_time=1.0)
            c.wait_until("circuit")
            self.play(*during(fn.static.animate.shift(FAN_O2 - FAN_O), 0, 0.7),
                      *during(cap.animate.shift(FAN_O2 - FAN_O), 0, 0.7),
                      *during(appear(circ.drawing, shift=None), 0.45, 1.0), run_time=1.5)
            c.wait_until("voltage")
            self.play(*appear(*circ.labels, lag=0.35), run_time=1.6)
            c.wait_until("algebra")
            self.play(*appear(alg), run_time=1.0)  # early: the line's headline, read at its end
            c.wait_until("each derivative")
            self.play(*flash([lb[1] for lb in circ.labels], color=YELLOW, run_time=1.4, time_width=1.5))
        self.wait(1.2)
