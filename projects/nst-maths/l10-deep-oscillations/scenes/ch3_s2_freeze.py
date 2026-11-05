"""Chapter 3, scene 2: one arrow (ride along and it freezes: x = Re[A e^{iωt}]). Clips c3.freeze.1 – c3.freeze.4.

Also chapter 3's PLANE KIT (load_scene("ch3_s2_freeze")), module-level and free of scene state.
`t` (model seconds), `rot` (plane rotation, rad) and `zs` (zoom, 1 = 0.42 per cm) take a
ValueTracker (or anything with .get_value(): the drawing redraws every frame) or a plain number.
  Constants  PLANE3_O (-3.2, 0.6) (ak.PLANE_O raised 0.2: see below), CM = 0.42 (scene units per
             cm), S3 = CM / ak.PLANE_R (the arrow kit's `scale` for this plane), A3 = 3 - 4j,
             R3 = 5, PHI3 = arg A3 (-0.927), OMEGA3 = 3, CLOCK = 2/3 (model s per video s:
             2 rad/s on screen), PERIOD3 = 2π/3, RG / RA (grid / axes radius in scene units).
  pt(z, zs=1, rot=0)              scene point of complex z (in cm).
  plane3(rot=0, zs=1)             DIM grid (1 cm squares, clipped to a disc), axes, the DIM circle
                                  of radius 5; turns with rot, zooms with zs. .grid .axes .circle
  plane_labels()                  "Re" / "Im" (static, for rot = 0). .re .im
  arrow3(t, rot=0, zs=1, amp=A3, color=GOLD, width=6, op=1)   the arrow amp·e^{iωt}.
  shadow3(t, rot=0, zs=1, amp=A3, glow=0)   DIM dashed drop line + BLUE shadow dot. .line .dot
  spring3(t, zs=1, amp=A3, op=1)  ch1's spring along the real axis (ak.spring_on_axis), the
                                  block's centre on the shadow.
  frozen_A(label=True)            the still GOLD A at -53° + its GOLD "A" label. .arrow .label
  amp_pin()                       the chapter's pin x(t) = Re[A e^{iωt}] (kit.pinned, PIN_POS).
  amp_caption(size=44)            the same formula unplaced (it shrinks into amp_pin's slot).
  MOVE_M7, move_m7()              M7's move card (kit.move_card).
  clock3(t)                       tracker t advances at t.clock_rate (model s per video s; 0 = still).
  Legend: E_A, E_ANGLE3, E_MIRROR, E_RULE; ENTRIES3_0 (start), ENTRIES3 (end), LEG_ROWS3 = 4.
  handover_shot()                 the last frame (s3 opens on it): plane, labels, spring at x = 3,
                                  frozen A, shadow, M7 card, amp_pin, legend.
                                  .plane .labels .spring .frozen .shadow .card .pin .legend
Z order as the arrow kit: plane -4, arrows -2, marks -1.7, legend panel -1.
Why y = 0.6, not 0.4: the radius-5 plane reaches 2.2 below its origin; at 0.4 it would run 0.1 into
the two-column legend (top -1.69).
"""
# style: 2
# handover: next
import cmath
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene, manifest  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

kit = load_scene("ch1_s2_tools")
ak = load_scene("ch2_s3_velocity")

# ═══════════════════════════════ chapter 3's plane kit (shared) ═══════════════════════════════
PLANE3_O = np.array([ak.PLANE_O[0], 0.6, 0.0])
CM = 0.42
S3 = CM / ak.PLANE_R
A3 = 3 - 4j
R3 = abs(A3)
PHI3 = cmath.phase(A3)
OMEGA3 = 3.0
CLOCK = 2.0 / 3.0
PERIOD3 = TAU / OMEGA3
RG, RA = 2.15, 2.2
Z_PLANE, Z_GOLD, Z_MARK, Z_LABEL = -4, -2, -1.7, 1


class Live:
    """A number source for the drawings: get_value() calls f()."""
    def __init__(self, f):
        self.f = f

    def get_value(self):
        return self.f()


def _v(x):
    return x.get_value() if hasattr(x, "get_value") else float(x)


def _dyn(build, *args):
    if any(hasattr(a, "get_value") for a in args):
        return always_redraw(build)
    return build()


def _fade(m, op):
    """Scale every part's stroke and fill opacity by op (keeps the block's 0.3 fill ratio)."""
    if op >= 0.999:
        return m
    for sm in m.family_members_with_points():
        sm.set_stroke(opacity=sm.get_stroke_opacity() * op)
        sm.set_fill(opacity=sm.get_fill_opacity() * op)
    return m


def pt(z, zs=1.0, rot=0.0, origin=PLANE3_O):
    z = complex(z) * cmath.exp(1j * rot)
    return np.array(origin, dtype=float) + CM * zs * np.array([z.real, z.imag, 0.0])


def plane3(rot=0.0, zs=1.0, origin=PLANE3_O):
    def build():
        a, s = _v(rot), CM * _v(zs)
        c, sn = math.cos(a), math.sin(a)
        o = np.array(origin, dtype=float)

        def P(x, y):
            return o + np.array([c * x - sn * y, sn * x + c * y, 0.0])
        lines = []
        n = int(RG // s)
        for k in range(-n, n + 1):
            d = k * s
            h = math.sqrt(max(RG * RG - d * d, 0.0))
            if k == 0 or h < 0.03:
                continue
            lines += [Line(P(d, -h), P(d, h)), Line(P(-h, d), P(h, d))]
        grid = VGroup(*lines).set_stroke(DIM, 1, opacity=0.35)
        axes = VGroup(Line(P(-RA, 0), P(RA, 0)), Line(P(0, -RA), P(0, RA))).set_stroke(DIM, 2.5)
        circle = Circle(radius=R3 * s).move_to(o).set_stroke(DIM, 2.5)
        g = VGroup(grid, axes, circle)
        g.set_z_index(Z_PLANE)
        g.grid, g.axes, g.circle = grid, axes, circle
        return g
    return _dyn(build, rot, zs)


def plane_labels(origin=PLANE3_O):
    o = np.array(origin, dtype=float)
    re = T("Re", size=28, color=DIM).next_to(o + RA * RIGHT, RIGHT, buff=0.45)   # clear of the block at x = 5
    im = T("Im", size=28, color=DIM).next_to(o + RA * UP, RIGHT, buff=0.15).shift(0.2 * DOWN)
    g = VGroup(re, im)
    g.re, g.im = re, im
    return g


def _zt(t, amp=A3):
    return complex(amp) * cmath.exp(1j * OMEGA3 * _v(t))


def arrow3(t, rot=0.0, zs=1.0, amp=A3, color=GOLD, width=6, op=1.0, z=Z_GOLD):
    def build():
        a = ak.arrow_between(PLANE3_O, pt(_zt(t, amp), _v(zs), _v(rot)), color, width, z)
        return _fade(a, _v(op))
    return _dyn(build, t, rot, zs, op)


def shadow3(t, rot=0.0, zs=1.0, amp=A3, glow=0.0):
    def build():
        zp = _zt(t, amp)
        s, r, g = _v(zs), _v(rot), _v(glow)
        tip, foot = pt(zp, s, r), pt(zp.real, s, r)
        if np.linalg.norm(tip - foot) > 0.05:
            ln = DashedLine(tip, foot, dash_length=0.08).set_stroke(DIM, 2)
        else:
            ln = Line(tip, foot).set_stroke(DIM, 2, opacity=0)
        col = interpolate_color(ManimColor(BLUE), ManimColor(WHITE), 0.4 * g)
        dot = Dot(foot, radius=0.09 + 0.06 * g, color=col).set_z_index(Z_MARK)
        grp = VGroup(ln, dot)
        grp.line, grp.dot = ln, dot
        return grp
    return _dyn(build, t, rot, zs, glow)


def spring3(t, zs=1.0, amp=A3, op=1.0):
    def build():
        g = ak.spring_on_axis(_v(t), omega=OMEGA3, offset=cmath.phase(amp), length=abs(amp) * S3,
                              scale=_v(zs), origin=PLANE3_O)
        return _fade(g, _v(op))
    return _dyn(build, t, zs, op)


def _a_label():
    lab = MathTex("A", font_size=44, color=GOLD)
    lab.next_to(pt(A3), RIGHT, buff=0.22)
    return lab


def frozen_A(label=True):
    arr = arrow3(0.0)
    g = VGroup(arr)
    g.arrow, g.label = arr, None
    if label:
        g.label = _a_label()
        g.add(g.label)
    return g


CAP_TEX = [r"x(t)", "=", r"\mathrm{Re}", r"\big[\,", "A", r"\,", r"e^{i\omega t}", r"\,\big]"]


def _color_cap(f):
    for i, col in ((0, BLUE), (2, BLUE), (4, GOLD), (6, GOLD)):
        f[i].set_color(col)
    return f


def amp_caption(size=44):
    return _color_cap(MathTex(*CAP_TEX, font_size=size))


def amp_pin():
    """x(t) = Re[A e^{iωt}] pinned at top centre (x, Re BLUE; A, e^{iωt} GOLD). .formula"""
    pin = kit.pinned(CAP_TEX)
    _color_cap(pin.formula)
    return pin


MOVE_M7 = "Ride along and the arrow holds still: that frozen arrow, A, is the swing."


def move_m7():
    return kit.move_card(MOVE_M7)


def clock3(t):
    t.clock_rate = 0.0
    t.add_updater(lambda m, dt: m.increment_value(m.clock_rate * dt))
    return t


E_A = (r"A", GOLD, "frozen arrow")
E_ANGLE3 = (r"\omega t", YELLOW, "angle")
E_MIRROR = (r"A^{*}", PURPLE, "mirror")
E_RULE = (r"\ddot{x} = -\omega^2 x", FG, "rule")
ENTRIES3_0 = [ak.E_X, ak.E_W, ak.E_ARROW]
ENTRIES3 = ENTRIES3_0 + [E_A, E_ANGLE3, E_RULE, E_MIRROR]
LEG_ROWS3 = 4


def handover_shot():
    pl = plane3()
    labs = plane_labels()
    sp = spring3(0.0)
    fr = frozen_A()
    sh = shadow3(0.0)
    card = move_m7()
    pin = amp_pin()
    leg = kit.legend(ENTRIES3, LEG_ROWS3)
    g = VGroup(pl, labs, sp, fr, sh, card, pin, leg)
    (g.plane, g.labels, g.spring, g.frozen, g.shadow, g.card, g.pin,
     g.legend) = pl, labs, sp, fr, sh, card, pin, leg
    return g


# ═══════════════════════════════ the scene ═══════════════════════════════
TAG_POS = np.array([-6.6, 3.05, 0])       # Fig. 24 tag, later "beyond the notes" (UL corner)
GLYPH_POS = np.array([-6.1, 2.3, 0])
RO_POS = np.array([-0.9, 2.6, 0])     # live readouts (left edge 1.0 left of it)        # live readouts, top right of the plane
LOW_POS = np.array([-1.5, -2.3, 0])       # under the plane, right of the one-column legend
RED_LEN = 1.6                             # true length ω²·5 = 45 cm = 18.9 units
BLOCK_HALF, BLOCK_HALF_H = ak.spr.BLOCK_W / 2, ak.spr.BLOCK_H / 2   # the block on the real axis
SPRING_HALF = 0.32                        # the coil's half-height about the axis
WALL_X = PLANE3_O[0] + ak.spr.SPRING_WALL_X - ak.spr.SPRING_REST_X
Y_L1, Y_TERM, Y_L2 = 1.25, 0.55, -0.15
CAP_Y, CAP_TAG_Y, WORDS_Y = -1.0, -1.58, -1.95
CAP_SIZE = 52
HOLD_END = 2.0                            # after the last word, before the column clears


def _gap(cid):
    return manifest()[cid].get("gap_after", NarratedScene.gap)


def _mark(cid, m):
    return manifest()[cid]["marks"][m]


def _side(p0, p1, mob, sign=1, buff=0.15):
    """Centre for mob beside the segment p0→p1, at its middle, on the left (sign=1) side."""
    d = p1 - p0
    L = np.linalg.norm(d)
    if L < 1e-6:
        return p0 + buff * UP
    u = d / L
    n = sign * np.array([-u[1], u[0], 0.0])
    reach = 0.5 * (abs(n[0]) * mob.width + abs(n[1]) * mob.height)
    return (p0 + p1) / 2 + n * (buff + reach)


def mgr_glyph(rot, center=GLYPH_POS, r=0.3):
    """A small DIM merry-go-round seen from above: rim, three spokes and riders turning with rot,
    and a clockwise arrow round it."""
    def build():
        a = _v(rot)
        c = np.array(center, dtype=float)
        rim = Circle(radius=r).move_to(c).set_stroke(DIM, 2)
        dirs = [np.array([math.cos(a + k * TAU / 3), math.sin(a + k * TAU / 3), 0]) for k in range(3)]
        spokes = VGroup(*[Line(c, c + r * d) for d in dirs]).set_stroke(DIM, 2)
        riders = VGroup(*[Dot(c + 0.8 * r * d, radius=0.05, color=DIM) for d in dirs])
        arc = Arc(radius=r + 0.14, start_angle=0.8 * PI, angle=-0.55 * PI, arc_center=c)
        arc.set_stroke(DIM, 2)
        arc.add_tip(tip_length=0.12, tip_width=0.12)
        arc.get_tip().set_fill(DIM, 1).set_stroke(DIM, 1)
        return VGroup(rim, spokes, riders, arc)
    return _dyn(build, rot)


def live_readout(label_tex, fn, unit, color, size, places, op, pos, head=None):
    """A readout rebuilt every frame from fresh parts, its left edge fixed (left edge of the
    number line at pos[0] - 1.0), faded by tracker op; an optional text line `head` above it."""
    lab = MathTex(label_tex, font_size=size * 1.25, color=color)
    un = T(unit, size=size, color=color) if unit else None
    hd = head

    def build():
        num = T(f"{fn():.{places}f}", size=size * 1.2, color=color)   # one Text: no digit pairs
        l = lab.copy()
        num.next_to(l, RIGHT, buff=0.15).align_to(l, DOWN)
        parts = [l, num]
        if un is not None:
            u = un.copy().next_to(num, RIGHT, buff=0.04 if unit == "°" else 0.12)
            parts.append(u.align_to(num, UP if unit == "°" else DOWN))
        row = VGroup(*parts)
        row.move_to(pos, aligned_edge=LEFT).shift(1.0 * LEFT)
        g = row
        if hd is not None:
            h = hd.copy().next_to(row, UP, buff=0.14).align_to(row, LEFT)
            g = VGroup(h, row)
        return _fade(g, op.get_value())
    return always_redraw(build)


def _col_line(tex, color_idx, size=36):
    m = MathTex(*tex, font_size=size)
    for i, col in color_idx:
        m[i].set_color(col)
    return m


class Freeze(NarratedScene):
    def construct(self):
        self.t = ValueTracker(0.0)
        self.clk_base, self.clk_t0, self.clk_rate = 0.0, 0.0, 0.0
        self.t.add_updater(lambda m: m.set_value(self.clk_base + self.clk_rate * (self.time - self.clk_t0))
                           if self.clk_rate is not None else None)
        self.add(self.t)
        self.spinning = False
        self.rot = Live(lambda: -OMEGA3 * self.t.get_value() if self.spinning else 0.0)
        self.zs = ValueTracker(1.0)
        self.sp_op = ValueTracker(1.0)
        self.dot_glow = ValueTracker(0.0)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.handover()

    # ── clock control ────────────────────────────────────────────────────────────
    def aim(self, t_abs, tmod):
        """Trim the clock (a few %) so that at scene time t_abs the model time is ≡ tmod (mod one
        period); snap() lands it exactly. The clock reads the scene's own time (frame-exact), not
        summed dt's."""
        v0 = self.t.get_value()
        dt = max(t_abs - self.time, 1e-3)
        n = round((v0 + CLOCK * dt - tmod) / PERIOD3)
        v1 = tmod + n * PERIOD3
        while (v1 - v0) / dt < 0.6 * CLOCK:
            v1 += PERIOD3
        self.set_clock((v1 - v0) / dt)
        self._target = v1

    def set_clock(self, rate, value=None):
        self.clk_base = self.t.get_value() if value is None else value
        self.clk_t0 = self.time
        self.clk_rate = rate
        self.t.set_value(self.clk_base)

    def snap(self):
        self.set_clock(self.clk_rate, self._target)

    def live(self, *mobs):
        self.add(*mobs)
        return mobs

    # ── c3.freeze.1: any arrow obeys the rule ──────────────────────────────────────
    def clip1(self):
        with self.say("c3.freeze.1") as c:
            pl_s, sp_s = plane3(), spring3(0.0)
            self.labs = plane_labels()
            self.rule = ak.rule_pin()
            self.leg = kit.legend(ENTRIES3_0, LEG_ROWS3)
            self.play(FadeIn(pl_s), FadeIn(self.labs), FadeIn(sp_s), FadeIn(self.rule),  # early: the board returns
                      FadeIn(self.leg), run_time=1.2)
            gold_s, sh_s = arrow3(0.0), shadow3(0.0)
            self.fig = kit.tag("Fig. 24 · notes p. 108").move_to(TAG_POS, aligned_edge=UL)
            self.play(GrowArrow(gold_s), FadeIn(sh_s), *appear(self.fig), run_time=1.2)  # early: reference tag
            # go live: identical drawings, now driven by the clock
            self.remove(pl_s, sp_s, gold_s, sh_s)
            self.pl = plane3(self.rot, self.zs)
            self.spring = spring3(self.t, self.zs, op=self.sp_op)
            self.gold = arrow3(self.t, self.rot, self.zs)
            self.sh = shadow3(self.t, self.rot, self.zs, glow=self.dot_glow)
            self.add(self.pl, self.spring, self.gold, self.sh)
            t_spin = c.end + _gap("c3.freeze.1") + _mark("c3.freeze.2", "spin")
            self.aim(t_spin, 0.0)

            c.wait_until("any")
            self.unit = DashedVMobject(Circle(radius=CM).move_to(PLANE3_O), num_dashes=12)
            self.unit.set_stroke(FG, 2).set_z_index(Z_MARK)
            self.play(FadeIn(self.unit), run_time=1.0)

            c.wait_until("Does its shadow")
            q_op = ValueTracker(0.0)
            qbase = T("?", size=44, color=DIM)

            def qb():
                zp = _zt(self.t)
                p = (pt(zp) + pt(zp.real)) / 2
                m = qbase.copy().move_to(p + 0.32 * LEFT).set_z_index(Z_LABEL)
                return _fade(m, q_op.get_value())
            self.q = always_redraw(qb)
            self.add(self.q)
            self.play(q_op.animate.set_value(1.0), FlashAround(self.rule.formula, time_width=1.5),
                      run_time=1.5)

            c.wait_until("fan")
            self.red_op, self.red_glow = ValueTracker(0.0), ValueTracker(0.0)
            rlab = VGroup(MathTex(r"-\omega^2\,\times", font_size=36, color=RED),
                          T("not to scale", size=22, color=DIM)).arrange(DOWN, buff=0.08)

            def rb():
                d = -_zt(self.t) / R3
                end = PLANE3_O + RED_LEN * np.array([d.real, d.imag, 0.0])
                g = self.red_glow.get_value()
                col = interpolate_color(ManimColor(RED), ManimColor(WHITE), 0.35 * g)
                a = ak.arrow_between(PLANE3_O, end, col, 6 + 4 * g, -1.9)
                lab = rlab.copy()
                lab.move_to(_side((PLANE3_O + end) / 2, end, lab, sign=1)).set_z_index(Z_LABEL)
                return _fade(VGroup(a, lab), self.red_op.get_value())
            self.red = always_redraw(rb)
            self.add(self.red)
            self.play(q_op.animate.set_value(0.0), self.red_op.animate.set_value(1.0), run_time=1.2)
            self.remove(self.q)

            c.wait_until("minus omega squared")
            self.play(self.red_glow.animate(rate_func=there_and_back).set_value(1.0), run_time=1.2)

            c.wait_until("general")
            self.anyline = T("any length, any start", size=30, color=DIM).move_to(LOW_POS + 0.1 * UP)
            self.play(self.red_op.animate.set_value(0.0), FadeOut(self.unit),
                      *during(appear(self.anyline), 0.3, 1.0), run_time=1.5)
            self.remove(self.red)

    # ── c3.freeze.2: ride along, and the arrow freezes as A ───────────────────────────
    def clip2(self):
        with self.say("c3.freeze.2") as c:
            ang_op = ValueTracker(0.0)
            ang = live_readout(r"\text{angle} =",
                               lambda: math.degrees((PHI3 + OMEGA3 * self.t.get_value()
                                                     + self.rot.get_value()) % TAU),
                               "°", FG, 28, 0, ang_op, RO_POS)
            self.add(ang)
            self.play(ang_op.animate.set_value(1.0), run_time=1.0)

            c.wait_until("ride")
            self.card = move_m7()
            self.play(*appear(self.card), *disappear(self.fig, self.anyline, self.labs),
                      self.sp_op.animate.set_value(0.0), run_time=1.5)
            self.remove(self.spring)

            c.wait_until("spin")
            self.snap()
            self.set_clock(self.clk_rate, 0.0)
            self.spinning = True
            self.aim(c.end + _gap("c3.freeze.2"), 0.0)
            self.spin_op = ValueTracker(0.0)
            self.spin_ro = live_readout(r"\omega t =", lambda: (math.fmod(OMEGA3 * self.t.get_value(), TAU)
                                                               if self.spinning else 0.0), "rad", YELLOW,
                                        28, 2, self.spin_op, LOW_POS,
                                        head=T("turned backwards by", size=28, color=FG))
            self.add(self.spin_ro)
            self.glyph = mgr_glyph(self.rot)
            self.ptag = kit.tag("beyond the notes").move_to(TAG_POS, aligned_edge=UL)
            self.play(*during(ang_op.animate.set_value(0.0).build(), 0, 0.45),
                      *during(self.spin_op.animate.set_value(1.0).build(), 0.5, 1.0), FadeIn(self.glyph), *during(appear(self.ptag), 0.5, 1.0),
                      run_time=1.2)

            self.remove(ang)

            c.wait_until("why")
            self.l1 = _col_line([r"\text{ride along: }", r"\times\,", r"e^{-i\omega t}"], [(2, PURPLE)])
            kit.col_place(self.l1, 0).set_y(Y_L1)
            self.play(*appear(self.l1), run_time=1.2)

            c.wait_until("called the complex")
            word = T("complex amplitude", size=30, color=FG)
            box = SurroundingRectangle(word, color=YELLOW, buff=0.12).set_stroke(YELLOW, 2.5)
            self.term = VGroup(MathTex("A", font_size=40, color=GOLD), MathTex("=", font_size=40),
                               VGroup(box, word)).arrange(RIGHT, buff=0.2)
            kit.col_place(self.term, 0).set_y(Y_TERM)
            self.play(*appear(self.term), run_time=1.0)

            c.wait_until("capital")
            self.alab = _a_label()
            kit.legend_add(self, self.leg, E_A, run_time=min(1.2, c.until(floor=0.8)),
                           extra=appear(self.alab))

    # ── c3.freeze.3: let it go: x = Re[A e^{iωt}] ─────────────────────────────────────
    def clip3(self):
        with self.say("c3.freeze.3") as c:
            self.snap()
            self.set_clock(CLOCK, 0.0)
            self.spinning = False
            self.remove(self.glyph)
            self.glyph = mgr_glyph(0.0)
            self.add(self.glyph)
            self.ghost = _fade(arrow3(0.0, z=Z_GOLD - 0.1), 0.35)
            self.add(self.ghost)
            self.arc_op, self.arc_glow = ValueTracker(1.0), ValueTracker(0.0)

            def ab():
                a = math.fmod(OMEGA3 * self.t.get_value(), TAU)
                a = max(a, 1e-3)
                g = self.arc_glow.get_value()
                arc = Arc(radius=0.6, start_angle=PHI3, angle=a, arc_center=PLANE3_O)
                arc.set_stroke(interpolate_color(ManimColor(YELLOW), ManimColor(WHITE), 0.3 * g), 4 + 5 * g)
                arc.set_z_index(Z_MARK)
                return _fade(arc, self.arc_op.get_value())
            self.arc = always_redraw(ab)
            self.add(self.arc)
            self.add(self.spring)
            self.wt_op = ValueTracker(0.0)
            self.wt = live_readout(r"\omega t =", lambda: math.fmod(OMEGA3 * self.t.get_value(), TAU), "rad", YELLOW,
                                   28, 2, self.wt_op, RO_POS)
            self.add(self.wt)
            self.play(*during(self.spin_op.animate.set_value(0.0).build(), 0, 0.45),
                      *during(self.wt_op.animate.set_value(1.0).build(), 0.5, 1.0),
                      *appear(self.labs, shift=None), self.sp_op.animate.set_value(1.0), run_time=1.2)
            self.remove(self.spin_ro)

            c.wait_until("Multiplying by")
            self.lab_op = ValueTracker(0.0)
            glab = MathTex(r"A\,e^{i\omega t}", font_size=36, color=GOLD)

            def gb():
                # right of the arrow; pushed further out along the normal (continuous, no jumps)
                # while it would touch the block or the spring lying on the real axis
                zp = _zt(self.t)
                tip, foot = pt(zp), pt(zp.real)
                m = glab.copy()
                hw, hh = m.width / 2, m.height / 2
                bx, ay = BLOCK_HALF + 0.12, PLANE3_O[1]

                def clear(c):
                    xl, xr = c[0] - hw, c[0] + hw
                    if xr < WALL_X or xl > foot[0] + bx:
                        return True
                    band = (BLOCK_HALF_H + 0.12 if xr > foot[0] - bx and xl < foot[0] + bx
                            else SPRING_HALF + 0.12)
                    return abs(c[1] - ay) - hh >= band
                e = 0.0
                while e < 2.0 and not clear(_side(PLANE3_O, tip, m, sign=-1, buff=0.15 + e)):
                    e += 0.02
                m.move_to(_side(PLANE3_O, tip, m, sign=-1, buff=0.15 + e)).set_z_index(Z_LABEL)
                set_backstroke(m)   # reads cleanly over the faint ghost of A it passes
                return _fade(m, self.lab_op.get_value())
            self.glab = always_redraw(gb)
            self.add(self.glab)
            self.l2 = _col_line([r"\text{let go: }", r"\times\,", r"e^{i\omega t}"], [(2, GOLD)])
            kit.col_place(self.l2, 0).set_y(Y_L2)
            self.play(self.lab_op.animate.set_value(1.0), *appear(self.l2), run_time=1.2)

            c.wait_until("keeps its length")
            ring = Circle(radius=R3 * CM).move_to(PLANE3_O).rotate(PHI3).set_stroke(GOLD, 5)
            self.play(VShowPassingFlash(ring, time_width=0.5), run_time=1.5)

            c.wait_until("adds omega")
            kit.legend_add(self, self.leg, E_ANGLE3, run_time=1.2,
                           extra=[self.arc_glow.animate(rate_func=there_and_back).set_value(1.0)])

            c.wait_until("caption")
            self.cap = amp_caption(CAP_SIZE)
            kit.col_place(self.cap, 0).set_y(CAP_Y)
            self.cap_tag = kit.tag("(82) · notes p. 108")
            self.cap_tag.move_to([kit.COL_LEFT, CAP_TAG_Y, 0], aligned_edge=LEFT)
            self.play(*appear(self.cap), *during(appear(self.cap_tag), 0.5, 1.0), run_time=1.5)  # early: reference tag

            c.wait_until("read")
            items = []
            for txt in ("start at A", "turn by ωt", "take the shadow"):
                w = T(txt, size=24, color=DIM)
                b = SurroundingRectangle(w, buff=0.1, corner_radius=0.06).set_stroke(DIM, 1.5)
                items.append(VGroup(b, w))
            self.words = VGroup(*items).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            self.words.move_to([kit.COL_LEFT, WORDS_Y, 0], aligned_edge=UL)
            self.play(*appear(*items, lag=0.4), run_time=1.5)  # early: a list shown whole, then walked

            c.wait_until("Start at the frozen")
            b, w = items[0]
            self.play(w.animate.set_color(GOLD), b.animate.set_stroke(GOLD),
                      self.ghost.animate(rate_func=there_and_back).set_opacity(1.0),
                      FlashAround(self.alab, time_width=1.5), run_time=1.2)
            c.wait_until("turn it by")
            b, w = items[1]
            self.play(w.animate.set_color(YELLOW), b.animate.set_stroke(YELLOW),
                      self.arc_glow.animate(rate_func=there_and_back).set_value(1.0), run_time=1.2)
            c.wait_until("take the shadow")
            b, w = items[2]
            self.play(w.animate.set_color(BLUE), b.animate.set_stroke(BLUE),
                      self.dot_glow.animate(rate_func=there_and_back).set_value(1.0), run_time=1.2)

            c.wait_until("real")
            self.pk_op = ValueTracker(0.0)

            def pkb():
                zp = _zt(self.t)
                tip, foot = pt(zp), pt(zp.real)
                if np.linalg.norm(tip - foot) < 0.12:
                    return VMobject()
                a = ak.arrow_between(foot, tip, PINK, 7, -1.75)
                return _fade(a, self.pk_op.get_value())
            self.pk = always_redraw(pkb)
            self.add(self.pk)
            self.play(self.pk_op.animate.set_value(1.0), run_time=0.8)
            c.wait_until("throws the vertical")
            self.play(self.pk_op.animate.set_value(0.0), run_time=1.5)
            self.remove(self.pk)

    # ── c3.freeze.4: the mirror reading ───────────────────────────────────────────────
    def clip4(self):
        with self.say("c3.freeze.4") as c:
            # the caption becomes the chapter's pin (left, then up: clear of the move card); the rule
            # moves into the legend; the column, the arc, the ghost and the plane labels clear
            start = self.cap.copy()
            k = kit.PIN_SIZE / CAP_SIZE
            p0, p2 = self.cap.get_center(), np.array(kit.PIN_POS, dtype=float)
            p1 = np.array([p2[0], 1.5, 0.0])

            def ride_cap(m, a):
                a = smooth(a)
                p = p0 + (p1 - p0) * (a / 0.5) if a < 0.5 else p1 + (p2 - p1) * ((a - 0.5) / 0.5)
                m.become(start.copy().scale(1 + (k - 1) * min(1.0, a / 0.5)).move_to(p))
            leaving = disappear(self.rule, self.l1, self.term, self.l2, self.cap_tag, self.words,
                                self.ghost, self.alab, self.labs)
            kit.legend_add(self, self.leg, E_RULE, run_time=2.2,
                           extra=[*during(leaving, 0, 0.4),
                                  *during(UpdateFromAlphaFunc(self.cap, ride_cap), 0.4, 1.0),
                                  *during([self.arc_op.animate.set_value(0.0).build(),
                                           self.wt_op.animate.set_value(0.0).build(),
                                           self.lab_op.animate.set_value(0.0).build()], 0, 0.4)])
            self.remove(self.arc, self.wt, self.glab)

            self.key_g = MathTex(r"A\,e^{i\omega t}", font_size=36, color=GOLD).move_to(RO_POS + 0.2 * UP,
                                                                                       aligned_edge=LEFT)
            self.key_g.shift(1.0 * LEFT)
            self.play(self.zs.animate.set_value(0.5), self.sp_op.animate.set_value(0.0),
                      *during(appear(self.key_g), 0.5, 1.0), run_time=min(2.0, c.until("Reflect the arrow")))
            self.remove(self.spring)

            c.wait_until("Reflect the arrow")
            self.refl, self.pb, self.pu_op = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(1.0)

            def pub():
                zg = _zt(self.t)
                r = self.refl.get_value()
                tip_rel = complex(zg.real, zg.imag * (1 - 2 * r))
                base = self.pb.get_value() * zg
                s = self.zs.get_value()
                col = interpolate_color(ManimColor(GOLD), ManimColor(PURPLE), r)
                a = ak.arrow_between(pt(base, s), pt(base + tip_rel, s), col, 6, -1.9)
                return _fade(a, self.pu_op.get_value())
            self.pu = always_redraw(pub)
            self.add(self.pu)
            self.play(self.refl.animate.set_value(1.0), run_time=1.6)

            c.wait_until("turns the other way")
            self.key_p = MathTex(r"A^{*}e^{-i\omega t}", font_size=36, color=PURPLE)
            self.key_p.next_to(self.key_g, DOWN, buff=0.2).align_to(self.key_g, LEFT)
            kit.legend_add(self, self.leg, E_MIRROR, run_time=1.2, extra=appear(self.key_p))

            c.wait_until("sum")
            self.play(self.pb.animate.set_value(1.0), run_time=1.8)
            self.pv_op = ValueTracker(0.0)

            def pvb():
                zg = _zt(self.t)
                s = self.zs.get_value()
                tip, foot = pt(zg, s), pt(zg.real, s)
                if np.linalg.norm(tip - foot) < 0.14:
                    return VMobject()
                dx = 0.07 * RIGHT
                g = VGroup(ak.arrow_between(foot - dx, tip - dx, PINK, 5, -1.75),
                           ak.arrow_between(tip + dx, foot + dx, PINK, 5, -1.75))
                return _fade(g, self.pv_op.get_value())
            self.pv = always_redraw(pvb)
            self.add(self.pv)
            self.play(self.pv_op.animate.set_value(1.0), run_time=0.8)
            self.wait(min(1.0, c.until("So the sum sits", floor=0.0)))
            self.play(self.pv_op.animate.set_value(0.0), run_time=min(1.2, c.until("So the sum sits")))
            self.remove(self.pv)

            c.wait_until("So the sum sits")
            self.tx_op = ValueTracker(0.0)
            txl = MathTex("2x", font_size=36, color=BLUE)

            def txb():
                s = self.zs.get_value()
                p = pt(2 * _zt(self.t).real, s)
                d = Dot(p, radius=0.1, color=BLUE).set_z_index(Z_MARK)
                lab = txl.copy().next_to(p, UP, buff=0.2).set_z_index(Z_LABEL)
                return _fade(VGroup(d, lab), self.tx_op.get_value())
            self.tx = always_redraw(txb)
            self.add(self.tx)
            self.play(self.tx_op.animate.set_value(1.0), run_time=1.2)
            c.wait_until("twice the shadow")
            self.play(self.dot_glow.animate(rate_func=there_and_back).set_value(1.0), run_time=1.2)

            c.wait_until("half")
            # land the arrow on A after the clip: a hold, 1.0 s clear, then a 2 s ease-out whose
            # initial speed is the clock's
            self.delta = CLOCK * 2.0 / 3.0
            self.aim(c.end + _gap("c3.freeze.4") + HOLD_END + 1.0, -self.delta)
            self.l3 = _col_line([r"x", "=", r"\tfrac{1}{2}", r"\Big(", r"A\,e^{i\omega t}", "+",
                                 r"A^{*}e^{-i\omega t}", r"\Big)"], [(0, BLUE), (4, GOLD), (6, PURPLE)],
                                size=40)
            kit.col_place(self.l3, 0).set_y(Y_TERM)
            self.play(*appear(self.l3), run_time=1.5)

            c.wait_until("tag")
            self.l3tag = kit.tag("beyond the notes").next_to(self.l3, DOWN, buff=0.25).align_to(self.l3, LEFT)
            self.play(FlashAround(self.ptag, time_width=1.5), run_time=1.5)
            c.wait_until(own_word=self.l3tag)
            self.play(*appear(self.l3tag), run_time=0.8)
            self.play(FlashAround(self.l3tag, time_width=1.5), run_time=1.2)


    # ── handover: the frozen A, as s3 opens ─────────────────────────────────────────────
    def handover(self):
        self.wait(HOLD_END)
        self.play(self.pu_op.animate.set_value(0.0), self.tx_op.animate.set_value(0.0),
                  *disappear(self.l3, self.l3tag, self.ptag, self.glyph, self.key_g, self.key_p), run_time=1.0)
        self.remove(self.pu, self.tx)
        self.snap()
        self.clk_rate = None                 # the clock lets go; the play below moves t
        self.add(self.spring)
        self.play(self.t.animate.set_value(self._target + self.delta), self.zs.animate.set_value(1.0),
                  self.sp_op.animate.set_value(1.0), rate_func=rate_functions.ease_out_cubic,
                  run_time=2.0)
        self.alab = _a_label()
        self.play(*appear(self.alab), FadeIn(self.labs), run_time=0.8)
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(1.2)
