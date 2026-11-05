"""Chapter 2, scene 3: a quarter turn ahead (d/dt e^{iωt} = iω e^{iωt}, and Euler from motion). Clips c2.vel.1 – c2.vel.5.

Also the chapter's ARROW KIT (load_scene("ch2_s3_velocity")), module-level and free of scene
state. Every `t` argument is a ValueTracker holding the time t in seconds (the drawing then
redraws itself every frame) or a plain number (a still drawing, e.g. for handover shots).
`base`, `length` and `glow` take a tracker or a number the same way.
  Geometry   OMEGA = 2; PLANE_O (origin, x = SPRING_REST_X = -3.2, y = 0.4); PLANE_R = 1.3 (unit
             circle radius); plane_point(z, scale=1, origin=PLANE_O) → the scene point of complex z.
  plane(scale=1, origin=PLANE_O, re_units=2, im_units=1.5, labels=True)
             DIM grid (half-unit squares), DIM axes, DIM unit circle, "Re" / "Im".
             .grid .axes .circle .re .im
  turning_arrow(t, omega=OMEGA, offset=0, length=1, color=GOLD, scale=1, origin=PLANE_O, width=6)
             the arrow length·e^{i(ωt+offset)} from the origin. The mirror e^{-iωt}: omega=-OMEGA,
             color=PURPLE. The -i sine arrow: offset=-PI/2.
  velocity_arrow(t, base=1, omega, offset, length, color=GREEN, ..., glow=0)
             iω × (that arrow); base=1 starts it at the tip, base=0 at the origin (animate a base
             tracker 1 → 0 to slide it in). Its true length: ω × length.
  accel_arrow(t, base=1, …, color=RED)   -ω² × the arrow (length ω²), same conventions.
  right_angle(t, at_tip=True, omega, offset, length, size=0.2, glow=0, …)
             the right-angle mark between the arrow and its velocity (at the tip, or at the origin).
  angle_arc(t, omega, offset, radius=0.42, color=YELLOW, …)  the arc for the angle ωt (mod 2π).
  t_readout(t, size=30) "t = 0.60 s" (FG); wt_readout(t, omega, size=30) "ωt = 1.20 rad" (YELLOW).
  shadow(t, …)   DIM dashed drop line from the tip to Re, BLUE dot there. .line .dot
  spring_on_axis(t, …, zero=False)  ch1 s3's spring and block lying on the real axis, the block's
             centre on the shadow (the wall sits left of -2 at scale 1).
  arrow_between(start, end, color, width=6, z=-2)  the house arrow, for one-off still arrows.
  clock(t) / run(t, on)  make tracker t advance in real time while on (an updater; add t to the
             scene). Stop it, then play t.animate to an exact value for a deterministic freeze.
  rule_pin() the pinned rule ẍ = −ω²x (as ch2_s1_hook); lambda_box() s2's boxed λ = ±iω, small.
  velocity_caption() the boxed d/dt e^{iωt} = iω e^{iωt}. .line .box
  handover_shot() this scene's last frame (s4 opens on it). .plane .gold .green .pin .legend
             .card .caption
Z order: plane -4, arrows -2 .. -1.6 (under the legend panel, which is -1), so long arrows pass
behind the legend instead of over its text.
"""
# style: 2
# handover: next
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
spr = load_scene("ch1_s3_spring")

# ═══════════════════════════════ the arrow kit (shared) ═══════════════════════════════
OMEGA = 2.0
PLANE_O = np.array([spr.SPRING_REST_X, 0.4, 0])   # y 0.4 (not 0.6): the length-2 arrow at t = 0 clears the pin
PLANE_R = 1.3
Z_PLANE, Z_GOLD, Z_GREEN, Z_MARK = -4, -2, -1.8, -1.7


def _v(x):
    return x.get_value() if hasattr(x, "get_value") else float(x)


def _dyn(build, *args):
    """always_redraw(build) if any arg is a tracker, else one still build()."""
    if any(hasattr(a, "get_value") for a in args):
        return always_redraw(build)
    return build()


def plane_point(z, scale=1.0, origin=PLANE_O):
    z = complex(z)
    return np.array(origin, dtype=float) + PLANE_R * scale * np.array([z.real, z.imag, 0.0])


def phasor(t, omega=OMEGA, offset=0.0, length=1.0):
    """length · e^{i(ωt + offset)} as a complex number (t a number)."""
    return length * complex(math.cos(omega * t + offset), math.sin(omega * t + offset))


def arrow_between(start, end, color, width=6, z=Z_GOLD):
    a = Arrow(start, end, buff=0, stroke_width=width, tip_length=0.24,
              max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=40, color=color)
    a.set_z_index(z)
    return a


def plane(scale=1.0, origin=PLANE_O, re_units=2.0, im_units=1.5, labels=True):
    """The Argand plane: DIM grid (half-unit squares), axes, unit circle, Re / Im labels."""
    o = np.array(origin, dtype=float)
    u = PLANE_R * scale
    xs = np.arange(-re_units, re_units + 1e-6, 0.5)
    ys = np.arange(-im_units, im_units + 1e-6, 0.5)
    grid = VGroup(*[Line(o + [x * u, -im_units * u, 0], o + [x * u, im_units * u, 0]) for x in xs],
                  *[Line(o + [-re_units * u, y * u, 0], o + [re_units * u, y * u, 0]) for y in ys])
    grid.set_stroke(DIM, 1, opacity=0.35)
    ext = 0.25
    re_ax = Line(o + [-(re_units + ext) * u, 0, 0], o + [(re_units + ext) * u, 0, 0])
    im_ax = Line(o + [0, -(im_units + ext) * u, 0], o + [0, (im_units + ext) * u, 0])
    axes = VGroup(re_ax, im_ax).set_stroke(DIM, 2.5)
    circle = Circle(radius=u).move_to(o).set_stroke(DIM, 2.5)
    g = VGroup(grid, axes, circle)
    g.set_z_index(Z_PLANE)
    g.grid, g.axes, g.circle, g.re, g.im = grid, axes, circle, None, None
    if labels:
        re = T("Re", size=28 if scale >= 0.8 else 22, color=DIM)
        re.next_to(re_ax.get_end(), RIGHT, buff=0.15)
        im = T("Im", size=28 if scale >= 0.8 else 22, color=DIM)
        im.next_to(im_ax.get_end(), RIGHT, buff=0.15).shift(0.2 * DOWN)
        g.add(re, im)
        g.re, g.im = re, im
    return g


def turning_arrow(t, omega=OMEGA, offset=0.0, length=1.0, color=GOLD, scale=1.0, origin=PLANE_O,
                  width=6, z=Z_GOLD):
    """The arrow length·e^{i(ωt+offset)} from the origin (GOLD e^{iωt} by default)."""
    def build():
        p = phasor(_v(t), omega, offset, _v(length))
        return arrow_between(origin, plane_point(p, scale, origin), color, width, z)
    return _dyn(build, t, length)


def _derived_arrow(t, factor, base, omega, offset, length, color, scale, origin, width, z, glow):
    def build():
        p = phasor(_v(t), omega, offset, _v(length))
        start = plane_point(_v(base) * p, scale, origin)
        end = start + PLANE_R * scale * np.array([(factor * p).real, (factor * p).imag, 0.0])
        g = _v(glow)
        col = interpolate_color(ManimColor(color), ManimColor(WHITE), 0.35 * g)
        return arrow_between(start, end, col, width + 5 * g, z)
    return _dyn(build, t, base, length, glow)


def velocity_arrow(t, base=1.0, omega=OMEGA, offset=0.0, length=1.0, color=GREEN, scale=1.0,
                   origin=PLANE_O, width=6, z=Z_GREEN, glow=0.0):
    """iω × the arrow: at its tip (base=1) or from the origin (base=0). True length ω·length."""
    return _derived_arrow(t, 1j * omega, base, omega, offset, length, color, scale, origin, width, z,
                          glow)


def accel_arrow(t, base=1.0, omega=OMEGA, offset=0.0, length=1.0, color=RED, scale=1.0,
                origin=PLANE_O, width=6, z=Z_GREEN, glow=0.0):
    """-ω² × the arrow: at its tip (base=1) or from the origin (base=0). True length ω²·length."""
    return _derived_arrow(t, -omega ** 2, base, omega, offset, length, color, scale, origin, width,
                          z, glow)


def right_angle(t, at_tip=True, omega=OMEGA, offset=0.0, length=1.0, size=0.2, scale=1.0,
                origin=PLANE_O, color=FG, glow=0.0, z=Z_MARK):
    """Right-angle mark between the arrow and its velocity, at the tip or at the origin."""
    def build():
        p = phasor(_v(t), omega, offset, _v(length))
        d = np.array([p.real, p.imag, 0.0]) / max(abs(p), 1e-9)
        v = np.sign(omega) * np.array([-d[1], d[0], 0.0])
        if at_tip:
            corner, u1 = plane_point(p, scale, origin), -d
        else:
            corner, u1 = np.array(origin, dtype=float), d
        s = size * min(1.0, scale + 0.3)
        g = _v(glow)
        m = VMobject().set_points_as_corners([corner + s * u1, corner + s * (u1 + v), corner + s * v])
        m.set_stroke(interpolate_color(ManimColor(color), ManimColor(YELLOW), g), 2.5 + 4 * g)
        m.set_z_index(z)
        return m
    return _dyn(build, t, length, glow)


def angle_arc(t, omega=OMEGA, offset=0.0, radius=0.42, color=YELLOW, scale=1.0, origin=PLANE_O,
              width=4):
    """The arc for the angle ωt (wrapped to one turn), from offset."""
    def build():
        a = math.fmod(omega * _v(t), TAU)
        if abs(a) < 1e-3:
            a = 1e-3 if omega > 0 else -1e-3
        arc = Arc(radius=radius * min(1.0, scale + 0.3), start_angle=offset, angle=a,
                  arc_center=np.array(origin, dtype=float))
        arc.set_stroke(color, width).set_z_index(Z_MARK)
        return arc
    return _dyn(build, t)


def _readout(label_tex, fn, unit, color, size, places):
    lab = MathTex(label_tex, font_size=size * 1.25, color=color)
    num = DecimalNumber(fn(), num_decimal_places=places, font_size=size * 1.25, color=color)
    un = T(unit, size=size, color=color) if unit else VGroup()
    g = VGroup(lab, num, un)

    def place(m):
        m[1].set_value(fn())
        m[1].next_to(m[0], RIGHT, buff=0.15)
        m[1].align_to(m[0], DOWN)
        if len(m[2].points) or m[2].submobjects:
            m[2].next_to(m[1], RIGHT, buff=0.12)
            m[2].align_to(m[1], DOWN)
    place(g)
    g.add_updater(place)
    return g


def t_readout(t, size=30):
    """"t = 0.60 s" (FG), live."""
    return _readout(r"t =", lambda: _v(t), "s", FG, size, 2)


def wt_readout(t, omega=OMEGA, size=30):
    """"ωt = 1.20 rad" (YELLOW), live."""
    return _readout(r"\omega t =", lambda: omega * _v(t), "rad", YELLOW, size, 2)


def shadow(t, omega=OMEGA, offset=0.0, length=1.0, scale=1.0, origin=PLANE_O):
    """DIM dashed drop line from the tip to the real axis and the BLUE shadow dot. .line .dot"""
    def build():
        p = phasor(_v(t), omega, offset, _v(length))
        tip = plane_point(p, scale, origin)
        foot = plane_point(p.real, scale, origin)
        if np.linalg.norm(tip - foot) > 0.05:
            ln = DashedLine(tip, foot, dash_length=0.08).set_stroke(DIM, 2)
        else:
            ln = Line(tip, foot).set_stroke(DIM, 2, opacity=0)
        dot = Dot(foot, radius=0.09, color=BLUE).set_z_index(Z_MARK)
        g = VGroup(ln, dot)
        g.line, g.dot = ln, dot
        return g
    return _dyn(build, t, length)


def spring_on_axis(t, omega=OMEGA, offset=0.0, length=1.0, scale=1.0, origin=PLANE_O, zero=False):
    """ch1 s3's spring and block lying on the real axis: the block's centre is the shadow."""
    def build():
        p = phasor(_v(t), omega, offset, _v(length))
        x_cm = PLANE_R * p.real / spr.SPRING_UNIT          # scene units at scale 1 → cm
        y = PLANE_O[1] - spr.BLOCK_H / 2
        g = spr.spring_drawing(x_cm, y=y, zero=zero)
        g.shift(np.array(origin, dtype=float) - PLANE_O)
        if abs(scale - 1) > 1e-6:
            g.scale(scale, about_point=np.array(origin, dtype=float))
        return g
    return _dyn(build, t, length)


def clock(t):
    """Make tracker t advance in real time while t.running is True (starts stopped)."""
    t.running = False

    def tick(m, dt):
        if m.running:
            m.increment_value(dt)
    t.add_updater(tick)
    return t


def run(t, on=True):
    t.running = on


def rule_pin():
    """The pinned rule ẍ = −ω²x (ẍ RED, x BLUE, ω FG), label "the rule" (as ch2_s1_hook)."""
    pin = kit.pinned([r"\ddot{x}", "=", r"-\omega^2", "x"], label="the rule")
    pin.formula[0].set_color(RED)
    pin.formula[3].set_color(BLUE)
    return pin


def lambda_box(size=30):
    """s2's boxed λ = ±iω (i PINK), small. .line .box"""
    line = MathTex(r"\lambda", "=", r"\pm", "i", r"\omega", font_size=size)
    line[3].set_color(PINK)
    box = SurroundingRectangle(line, color=YELLOW, buff=0.14).set_stroke(YELLOW, 2.5)
    g = VGroup(line, box)
    g.line, g.box = line, box
    return g


def velocity_caption(size=40):
    """The boxed d/dt e^{iωt} = iω e^{iωt}: left side GREEN, e^{iωt} GOLD, i PINK, ω FG. .line .box"""
    line = MathTex(r"\frac{d}{dt}\,", r"e^{i\omega t}", "=", "i", r"\omega", r"\,", r"e^{i\omega t}",
                   font_size=size)
    line[0].set_color(GREEN)
    line[1].set_color(GREEN)
    line[3].set_color(PINK)
    line[6].set_color(GOLD)
    box = SurroundingRectangle(line, color=YELLOW, buff=0.16).set_stroke(YELLOW, 3)
    g = VGroup(line, box)
    g.line, g.box = line, box
    return g


# Legend
E_X = (r"x", BLUE, "displacement")
E_W = (r"\omega", FG, "turning rate")
E_T = (r"t", FG, "time")
E_LAM = (r"\lambda", FG, "trial rate")
E_ARROW = (r"e^{i\omega t}", GOLD, "turning arrow")
E_ANGLE = (r"\omega t", YELLOW, "its angle")
ENTRIES0 = [E_X, kit.E_XD, kit.E_XDD, E_W, E_T, E_LAM]
ENTRIES = ENTRIES0 + [E_ARROW, E_ANGLE]
LEG_ROWS = 4

MOVE_M5 = "Differentiating a turning arrow: a quarter turn ahead, stretched by ω"
T_END = (40 * DEGREES) / OMEGA       # the last frame: GOLD at 40°, GREEN at 130°
CAPTION_I = 0.22                        # caption's final column line


def caption_final():
    cap = velocity_caption()
    kit.col_place(cap, CAPTION_I)
    return cap


def handover_shot():
    """Last frame of s3 = first of s4: the plane, GOLD e^{iωt} at 40° and its GREEN velocity from
    the origin at 130° (still), move card M5, the pinned rule, the legend, the boxed caption at the
    top of the right column. .plane .gold .green .pin .legend .card .caption"""
    pl = plane()
    gold = turning_arrow(T_END)
    green = velocity_arrow(T_END, base=0.0)
    pin = rule_pin()
    leg = kit.legend(ENTRIES, LEG_ROWS)
    card = kit.move_card(MOVE_M5)
    cap = caption_final()
    g = VGroup(pl, gold, green, pin, leg, card, cap)
    g.plane, g.gold, g.green, g.pin, g.legend, g.card, g.caption = pl, gold, green, pin, leg, card, cap
    return g


# ═══════════════════════════════ the scene ═══════════════════════════════
T_ASK = 5 * PI / 6          # t mod π at the {ask} freeze: the arrow at -60°
T_EULER = 50 * DEGREES / OMEGA   # the converse dot's freeze for Euler's legs (50°)
CHECK_SIZE = 32


def _ci(y):
    """Column index of a line centred at y."""
    return (kit.COL_TOP - y) / kit.COL_PITCH


def _cj(y):
    """step_label index whose label sits at y."""
    return (kit.COL_TOP - y) / kit.COL_PITCH + 0.5


class Velocity(NarratedScene):
    def construct(self):
        self.t = clock(ValueTracker(0.0))
        self.add(self.t)
        self.pin = rule_pin()
        self.add(self.pin)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()

    # ── c2.vel.1: the turning arrow ───────────────────────────────────────────────
    def clip1(self):
        t = self.t
        self.pl = plane()
        self.leg = kit.legend(ENTRIES0, LEG_ROWS)
        self.lam = lambda_box()
        kit.col_place(self.lam, 0)
        with self.say("c2.vel.1") as c:
            self.play(*appear(self.pl, self.leg, self.lam, shift=None, lag=0.15),  # early: the board
                      run_time=1.2)
            self.gold = turning_arrow(t)
            glab = MathTex("e^{", "i", r"\omega t}", font_size=44, color=GOLD)
            glab[1].set_color(PINK)
            glab.next_to(plane_point(1), UR, buff=0.12)
            self.play(GrowArrow(self.gold), *appear(glab), run_time=1.5)
            c.wait_until("seen that")
            self.fig = kit.tag("Fig. 24 · notes p. 108")
            self.fig.move_to([-6.5, -1.28, 0], aligned_edge=LEFT)
            set_backstroke(self.fig, width=5)
            kit.legend_add(self, self.leg, E_ARROW, run_time=1.2)
            c.wait_until("length one")
            self.play(VShowPassingFlash(self.pl.circle.copy().set_stroke(GOLD, 6), time_width=0.5),
                      *appear(self.fig), run_time=1.6)
            c.wait_until("angle")
            self.arc = angle_arc(t)
            self.tr = t_readout(t).move_to([kit.COL_LEFT, 3.05, 0], aligned_edge=LEFT)
            self.wr = wt_readout(t).move_to([kit.COL_LEFT, 2.5, 0], aligned_edge=LEFT)
            self.play(FadeIn(self.arc), *appear(self.tr, self.wr, lag=0.3), *disappear(glab),
                      run_time=1.2)
            kit.legend_add(self, self.leg, E_ANGLE, run_time=1.2)
            # turn in real time, landing on the {ask} freeze at -60°
            avail = c.until("ask", floor=0)
            k = max(0, math.floor((avail - T_ASK) / PI))
            t1 = T_ASK + k * PI
            if avail > t1:
                self.wait(avail - t1)
            self.play(t.animate.set_value(t1), rate_func=linear, run_time=t1)
            self.q = T("?", size=56, color=YELLOW).move_to(plane_point(1.45 * phasor(t1)))
            self.play(*appear(self.q, shift=None), run_time=0.8)

    # ── c2.vel.2: the velocity arrow, then 2i ─────────────────────────────────────
    def clip2(self):
        t = self.t
        self.base = ValueTracker(1.0)
        self.add(self.base)
        self.green_glow = ValueTracker(0.0)
        self.green = velocity_arrow(t, base=self.base, glow=self.green_glow)
        mark_tip = right_angle(t, at_tip=True)
        with self.say("c2.vel.2") as c:
            self.play(*disappear(self.q), run_time=0.5)
            self.play(GrowArrow(self.green), FadeIn(mark_tip), run_time=1.5)
            t1 = t.get_value()
            self.play(t.animate.set_value(t1 + PI), rate_func=linear, run_time=PI)
            c.wait_until("ahead")
            tip = plane_point(phasor(t.get_value()))
            ahead = T("¼ turn ahead", size=30, color=FG).move_to([-1.35, -1.08, 0])
            self.play(*appear(ahead), FlashAround(mark_tip, color=YELLOW, time_width=1.5),
                      run_time=1.4)
            c.wait_until("speed")
            g_end = tip + PLANE_R * OMEGA * np.array([-math.sin(OMEGA * t.get_value()),
                                                      math.cos(OMEGA * t.get_value()), 0])
            speed = T("speed = 2", size=34, color=GREEN)
            speed.move_to([kit.COL_LEFT, g_end[1] + 0.05, 0], aligned_edge=LEFT)
            self.play(*appear(speed), run_time=1.0)
            c.wait_until("each second")
            note = kit.tag("arc each second = radius 1 × angle 2")
            note.next_to(speed, DOWN, buff=0.22, aligned_edge=LEFT)
            self.play(*appear(note), run_time=1.0)
            c.wait_until("slide")
            # freeze at t = 0: run the clock back, then slide the arrow to the centre
            self.play(*during([FadeOut(mark_tip)], 0, 0.25), *during(disappear(ahead), 0, 0.3),
                      t.animate.set_value(0.0), run_time=2.0)
            self.play(self.base.animate.set_value(0.0), run_time=1.5)
            c.wait_until("it points straight up")
            top = plane_point(2j)
            lab2i = MathTex("2", "i", font_size=40)
            lab2i[1].set_color(PINK)
            lab2i.next_to(top, LEFT, buff=0.25).shift(0.12 * DOWN)
            self.play(*appear(lab2i), run_time=1.0)
            c.wait_until("product")
            # a GOLD copy turns a quarter turn (× i), then stretches by 2
            rot, st = ValueTracker(0.0), ValueTracker(1.0)
            self.add(rot, st)
            copy = always_redraw(lambda: arrow_between(
                PLANE_O, plane_point(st.get_value() * complex(math.cos(rot.get_value()),
                                                              math.sin(rot.get_value()))),
                GOLD, 6, -1.9))
            self.add(copy)
            self.mark_glow = ValueTracker(0.0)
            self.mark_o = right_angle(t, at_tip=False, glow=self.mark_glow)
            times_i = MathTex(r"\times", "i", font_size=40, color=PINK)
            times_i.move_to(plane_point(1.55 * complex(math.cos(PI / 4), math.sin(PI / 4))))
            self.play(rot.animate.set_value(PI / 2), *appear(times_i), run_time=1.6)
            self.play(FadeIn(self.mark_o), self.mark_glow.animate(rate_func=there_and_back)
                      .set_value(1.0), run_time=1.2)
            times_2 = MathTex(r"\times", "2", font_size=40, color=FG)
            times_2.next_to(plane_point(1.45j), LEFT, buff=0.3)
            self.play(st.animate.set_value(2.0), *appear(times_2), run_time=1.5)
            self.extras = [times_i, times_2, lab2i, speed, note]
            self.copy = copy

    # ── c2.vel.3: the move, the caption, read it back ─────────────────────────────
    def clip3(self):
        t = self.t
        with self.say("c2.vel.3") as c:
            c.wait_until("for any omega")
            self.remove(self.copy)
            self.play(*disappear(*self.extras, self.tr, self.wr), FadeOut(self.arc), run_time=1.0)
            c.wait_until("move")
            run(t, True)
            self.card = kit.move_card(MOVE_M5)
            c.wait_until(own_word=self.card.body[0])
            self.play(*appear(self.card), run_time=1.2)
            c.wait_until("caption")
            self.cap = velocity_caption()
            kit.col_place(self.cap, 1.45)
            self.cap_tag = kit.tag("notes p. 109", self.cap, RIGHT)
            self.play(*appear(self.cap.line), GrowFromCenter(self.cap.box), run_time=1.5)
            self.play(*appear(self.cap_tag, shift=None), run_time=0.8)
            c.wait_until("eye is the quarter turn")
            self.play(self.mark_glow.animate(rate_func=there_and_back).set_value(1.0),
                      FlashAround(self.cap.line[3], color=PINK, time_width=1.5), run_time=1.6)
            c.wait_until("omega is the stretch")
            self.play(self.green_glow.animate(rate_func=there_and_back).set_value(1.0),
                      FlashAround(self.cap.line[4], color=YELLOW, time_width=1.5), run_time=1.6)
            c.wait_until("rule")
            link_a = MathTex(r"\dot{x}", "=", r"\lambda\, e^{\lambda t}", font_size=32, color=DIM)
            link_b = MathTex(r"\lambda", "=", "i", r"\omega", font_size=32)
            link_b[2].set_color(PINK)
            link_w = T("with", size=26, color=DIM)
            self.link = VGroup(link_a, link_w, link_b).arrange(RIGHT, buff=0.3)
            kit.col_place(self.link, 2.75)
            self.play(*appear(link_a, link_w, link_b, lag=0.3),
                      FlashAround(self.lam, color=YELLOW, time_width=1.5), run_time=1.6)

    # ── c2.vel.4: the converse, and Euler's formula ───────────────────────────────
    def clip4(self):
        t = self.t
        with self.say("c2.vel.4") as c:
            run(t, False)
            self.ctag = kit.corner_tag()
            self.play(*disappear(self.gold, self.green, self.mark_o, self.fig), run_time=0.8)
            self.play(*appear(self.ctag, shift=None), run_time=0.8)  # early: tag on the new topic
            c.wait_until("suppose")
            t2 = ValueTracker(0.0)
            self.add(t2)
            dot = always_redraw(lambda: Dot(plane_point(phasor(t2.get_value())), radius=0.11,
                                            color=GOLD).set_z_index(Z_MARK))
            pos = always_redraw(lambda: Line(PLANE_O, plane_point(phasor(t2.get_value())))
                                .set_stroke(GOLD, 3, opacity=0.55).set_z_index(Z_GOLD))
            self.play(FadeIn(dot, scale=0.5), Create(pos), run_time=1.0)
            r1 = VGroup(T("velocity", size=30, color=GREEN), T("=", size=30))
            r1.arrange(RIGHT, buff=0.15)
            r2 = VGroup(MathTex("i", r"\omega", font_size=38), T("×", size=30),
                        T("position", size=30, color=GOLD)).arrange(RIGHT, buff=0.15)
            r2[0][0].set_color(PINK)
            rule = VGroup(r1, r2).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            rule.move_to([-6.45, -1.05, 0], aligned_edge=LEFT)
            for m in (*r1, *r2):
                set_backstroke(m, width=5)
            c.wait_until(own_word=r1[0])
            self.play(*appear(r1), run_time=1.0)
            c.wait_until(own_word=r2[2])
            self.play(*appear(r2), run_time=1.0)
            green2 = velocity_arrow(t2)
            self.play(GrowArrow(green2), run_time=1.5)
            c.wait_until("right angles")
            mark2 = right_angle(t2, at_tip=True)
            self.play(FadeIn(mark2), run_time=0.8)
            length = _readout(r"\text{length} =", lambda: abs(complex(*(
                (plane_point(phasor(t2.get_value())) - PLANE_O)[:2])) / PLANE_R), "", FG, 30, 3)
            length.move_to([-1.15, -1.2, 0])
            c.wait_until("length")
            self.play(*appear(length), run_time=1.0)
            c.wait_until("circle")
            trail = always_redraw(lambda: Arc(radius=PLANE_R, start_angle=0,
                                              angle=max(1e-3, min(TAU - 1e-3,
                                                                  OMEGA * t2.get_value())),
                                              arc_center=PLANE_O).set_stroke(GOLD, 4)
                                  .set_z_index(Z_PLANE + 1))
            self.add(trail)
            # the column makes room: λ box and the link go, the caption rises to the top
            self.play(*during(disappear(self.lam, self.link), 0, 0.45),
                      *during([self.cap.animate.move_to(caption_final()),
                               self.cap_tag.animate.next_to(caption_final(), RIGHT, buff=0.2)],
                              0.2, 0.8), run_time=1.2)
            tgt = (TAU + 50 * DEGREES) / OMEGA
            self.play(t2.animate.set_value(tgt), rate_func=linear,
                      run_time=min(tgt, c.until("euler", floor=0.5)))
            c.wait_until("euler")
            p = phasor(t2.get_value())
            foot = plane_point(p.real)
            leg_c = Line(PLANE_O, foot).set_stroke(BLUE, 6).set_z_index(Z_MARK)
            leg_s = Line(foot, plane_point(p)).set_stroke(PINK, 6).set_z_index(Z_MARK)
            lc = MathTex(r"\cos\omega t", font_size=34, color=BLUE).next_to(leg_c, DOWN, buff=0.16)
            ls = MathTex(r"i\sin\omega t", font_size=34, color=PINK).next_to(leg_s, RIGHT, buff=0.16)
            set_backstroke(lc, width=5)
            set_backstroke(ls, width=5)
            self.play(GrowFromPoint(leg_c, PLANE_O), *appear(lc), run_time=1.3)
            self.play(GrowFromPoint(leg_s, foot), *appear(ls), run_time=1.3)
            self.eul = MathTex(r"e^{i\omega t}", "=", r"\cos\omega t", "+", r"i\sin\omega t",
                               font_size=CHECK_SIZE + 2)
            self.eul[0].set_color(GOLD)
            self.eul[2].set_color(BLUE)
            self.eul[4].set_color(PINK)
            kit.col_place(self.eul, _ci(0.42))
            n1 = kit.tag("Euler's formula, seen from motion")
            n2 = kit.tag("(71) · notes p. 97")
            VGroup(n1, n2).arrange(DOWN, buff=0.14, aligned_edge=LEFT).next_to(
                self.eul, DOWN, buff=0.2, aligned_edge=LEFT)
            c.wait_until("that's oiler's formula")
            self.play(*appear(self.eul), run_time=1.2)
            self.play(*appear(n1, n2, lag=0.3), run_time=1.0)  # early: on-screen it's "Euler"
            self.conv = [dot, pos, green2, mark2, trail, leg_c, leg_s, lc, ls, rule, length,
                         self.ctag]
            self.notes = [n1, n2]
            self.t2 = t2

    # ── c2.vel.5: the algebra agrees (reference) ──────────────────────────────────
    def clip5(self):
        t = self.t
        S = CHECK_SIZE
        with self.say("c2.vel.5") as c:
            t.set_value(self.t2.get_value())
            ref = kit.tag("reference", self.eul, RIGHT)
            self.play(*during(disappear(*self.conv), 0, 0.5),
                      *during([FadeIn(self.gold), FadeIn(self.green)], 0.45, 1.0), run_time=1.4)
            self.remove(self.t2)
            run(t, True)
            self.play(*appear(ref, shift=None), run_time=0.8)  # early: the tier tag
            c.wait_until("diff")
            l2 = MathTex(r"\frac{d}{dt}\, e^{i\omega t}", "=", r"-\omega\sin\omega t", "+",
                         r"i\omega\cos\omega t", font_size=S)
            kit.col_place(l2, _ci(-0.5))
            r2 = kit.step_label("chain rule, each part", _cj(0.04))
            self.play(*disappear(*self.notes), run_time=0.6)
            self.play(*appear(r2, l2, shift=None, lag=0.4), run_time=1.6)
            c.wait_until("factor")
            l3 = MathTex(r"-\omega\sin\omega t", "=", r"i\omega\cdot i\sin\omega t", font_size=S)
            kit.col_place(l3, _ci(-1.5))
            r3 = kit.step_label("i² = −1", _cj(-1.1))
            eq_x = l2[1].get_center()[0]
            l4 = MathTex("=", r"i\omega(\cos\omega t + i\sin\omega t)", font_size=S)
            kit.col_place(l4, _ci(-2.32))
            l4.shift((eq_x - l4[0].get_center()[0]) * RIGHT)
            r4 = kit.step_label("take out iω", _cj(-1.93))
            self.play(*appear(r3, l3, shift=None, lag=0.4), run_time=1.4)
            self.play(*appear(r4, l4, shift=None, lag=0.4), *set_alpha([self.eul], 0.4), run_time=1.4)
            c.wait_until("since eye times eye")
            l5 = MathTex("=", r"i\omega\, e^{i\omega t}", font_size=S + 2)
            kit.col_place(l5, _ci(-3.12))
            l5.shift((eq_x - l5[0].get_center()[0]) * RIGHT)
            box5 = SurroundingRectangle(l5[1], color=YELLOW, buff=0.14).set_stroke(YELLOW, 3)
            r5 = kit.step_label("Euler's formula again", _cj(-2.73))
            self.play(FlashAround(l3[2], color=PINK, time_width=1.5), *set_alpha([l2], 0.4),
                      run_time=1.2)
            self.play(*appear(r5, l5, shift=None, lag=0.4), GrowFromCenter(box5), run_time=1.5)
            lines = [self.eul, ref, l2, r2, l3, r3, l4, r4, l5, r5, box5, self.cap_tag]
        self.wait(3.3)      # the boxed result reads while the picture keeps turning
        # freeze on the handover shot: GOLD at 40°, the check lines cleared
        run(t, False)
        cur = t.get_value()
        target = T_END + math.ceil((cur - T_END) / PI + 1e-6) * PI
        dt = target - cur
        self.play(t.animate.set_value(target), *during(disappear(*lines), 0, min(1.0, 0.9 / dt)),
                  rate_func=linear, run_time=max(dt, 0.9))
        self.wait(1.0)
