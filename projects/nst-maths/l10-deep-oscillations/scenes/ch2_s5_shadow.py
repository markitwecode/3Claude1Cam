"""Chapter 2, scene 5: the shadow (Re of the turning arrow obeys the rule; it is cos ωt). Clips c2.shadow.1 – c2.shadow.4.

Shared: handover_shot() is this scene's last frame (s6 opens on it): the plane, GOLD e^{iωt} still
at 50° (T_HAND), its shadow (drop line, BLUE dot), the block on the axis, move card M6, the pinned
rule, the legend (FINAL_ENTRIES), and ak.lambda_box() at the top of the right column.
.plane .gold .shadow .spring .card .pin .legend .lam
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
ak = load_scene("ch2_s3_velocity")
hook = load_scene("ch2_s1_hook")
grav = load_scene("ch1_s5_gravity")
spr = load_scene("ch1_s3_spring")

OMEGA = ak.OMEGA
O = ak.PLANE_O
R = ak.PLANE_R
AX_Y = O[1]

MOVE_M6 = "Take the shadow: if the arrow obeys the rule, so does its shadow"
E_X_SHADOW = (r"x", BLUE, "the shadow")
FINAL_ENTRIES = [E_X_SHADOW] + list(ak.ENTRIES[1:])
T_HAND = 50 * DEGREES / OMEGA          # the last frame: GOLD at 50°


def handover_shot():
    """Last frame of s5 = first of s6 (still)."""
    pl = ak.plane()
    gold = ak.turning_arrow(T_HAND)
    sh = ak.shadow(T_HAND)
    sp = ak.spring_on_axis(T_HAND)
    card = kit.move_card(MOVE_M6)
    pin = ak.rule_pin()
    leg = kit.legend(FINAL_ENTRIES, ak.LEG_ROWS)
    lam = ak.lambda_box()
    kit.col_place(lam, 0)
    g = VGroup(pl, sp, gold, sh, card, pin, leg, lam)
    g.plane, g.gold, g.shadow, g.spring, g.card, g.pin, g.legend, g.lam = pl, gold, sh, sp, card, pin, leg, lam
    return g


# ═══════════════════════════════ helpers ═══════════════════════════════
COL_X = kit.COL_LEFT
CS = 32                                 # column MathTex size
UNROLL_T = (AX_Y - (-1.55)) / hook.WAVE_SEC     # seconds of wave on the time axis (4.33 s)
PEND_P = np.array([-6.1, 2.95, 0])
PEND_S = 0.6
PEND_L = 1.5
PEND_ARC_R = 1.2
SWING = 6.0                              # degrees


def _opacify(m, a):
    for sm in m.family_members_with_points():
        sm.set_stroke(opacity=sm.get_stroke_opacity() * a)
        sm.set_fill(opacity=sm.get_fill_opacity() * a)
    return m


def faded(m, op):
    """An always_redraw mobject whose opacity follows tracker op (fade it by animating op, so the
    drawing keeps moving while it fades)."""
    m.add_updater(lambda mm: _opacify(mm, op.get_value()))
    return m


def live(build, op):
    return faded(always_redraw(build), op)


def follow(mob, pos_fn, op):
    """A still label that tracks pos_fn() and whose opacity follows op."""
    def upd(m):
        m.move_to(pos_fn())
        m.set_opacity(op.get_value())
    mob.add_updater(upd)
    upd(mob)
    return mob


def at_col(mob, y):
    return mob.move_to([COL_X, y, 0], aligned_edge=LEFT)


def step_at(text, y):
    """kit.step_label whose label sits at y."""
    return kit.step_label(text, (kit.COL_TOP - y) / kit.COL_PITCH + 0.5)


def ph(t):
    return ak.phasor(t)


def tip(t):
    return ak.plane_point(ph(t))


def foot(t):
    return ak.plane_point(ph(t).real)


def tex(parts, colors, size=CS):
    m = MathTex(*parts, font_size=size)
    for i, col in colors.items():
        m[i].set_color(col)
    return m


def harrow(a, b, color, z=1):
    if np.linalg.norm(np.array(b) - np.array(a)) < 0.08:
        return VMobject()
    return ak.arrow_between(a, b, color, 6, z)


def readout(label_tex, fn, color, left, size=36):
    """A live "x = 0.36" readout (its label's left edge at `left`), rebuilt each frame from copies
    of per-character templates laid on fixed slots (no DecimalNumber, no TeX per value)."""
    lab = MathTex(label_tex, font_size=size, color=color).move_to(left, aligned_edge=LEFT)
    ref = MathTex("-", "8", ".", "8", "8", font_size=size, color=color)
    ref.next_to(lab, RIGHT, buff=0.15)
    ref.align_to(lab, DOWN)
    slots = [m.get_center() for m in ref]
    tpl = {ch: MathTex(ch, font_size=size, color=color) for ch in "-0123456789."}

    def glyph(ch, k):
        g = tpl[ch].copy()
        y = slots[k][1] if ch in "-." else slots[1][1]
        return g.move_to([slots[k][0], y, 0])

    def build():
        v = fn()
        txt = f"{abs(v):.2f}"
        if len(txt) != 4:
            txt = f"{min(abs(v), 9.99):.2f}"
        parts = [lab.copy()]
        sign = glyph("-", 0)
        if v >= -0.005:
            sign.set_opacity(0)   # kept in its slot: the family keeps its shape, no glyph jumps
        parts.append(sign)
        for k, ch in enumerate(txt):
            parts.append(glyph(ch, k + 1))
        return VGroup(*parts)
    return always_redraw(build)


class Shadow(NarratedScene):
    def construct(self):
        self.t = ak.clock(ValueTracker(0.0))
        self.add(self.t)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.finish()

    # ── c2.shadow.1: the line, the move, the shadow, the weight ─────────────────────
    def clip1(self):
        t = self.t
        self.pl = ak.plane()
        self.pin = ak.rule_pin()
        self.leg = kit.legend(ak.ENTRIES, ak.LEG_ROWS)
        self.gold = ak.turning_arrow(t)
        with self.say("c2.shadow.1") as c:
            self.play(*appear(self.pl, self.leg, self.pin, shift=None, lag=0.15),  # early: the board
                      GrowArrow(self.gold), run_time=1.2)
            ak.run(t, True)
            c.wait_until("line")
            brace = span_brace(ak.plane_point(-2.0), ak.plane_point(2.0), DOWN, DIM, buff=0.14)
            lab = T("x is real: it lives on this line", size=28, color=DIM, t2c={"x": BLUE})
            lab.next_to(brace, DOWN, buff=0.1)
            set_backstroke(lab, width=5)
            self.play(GrowFromCenter(brace), run_time=1.0)
            c.wait_until("real number", own_word=lab)
            self.play(*appear(lab), run_time=1.0)

            c.wait_until("move")
            self.card = kit.move_card(MOVE_M6)
            c.wait_until("take", own_word=self.card.body[0])
            self.play(*appear(self.card), run_time=1.2)
            self.fig = kit.tag("Fig. 24 · notes p. 108")
            self.fig.move_to([-6.5, -1.28, 0], aligned_edge=LEFT)
            set_backstroke(self.fig, width=5)
            self.play(*appear(self.fig, shift=None), run_time=0.8)

            c.wait_until("drop a line")
            self.play(*disappear(brace, lab), run_time=0.8)
            self.op_sh = ValueTracker(0.0)
            self.sh = faded(ak.shadow(t), self.op_sh)
            self.add(self.sh)
            self.play(self.op_sh.animate.set_value(1.0), run_time=1.5)
            c.wait_until("arrow's shadow")
            self.op_xl = ValueTracker(0.0)
            self.xl = follow(MathTex("x", font_size=38, color=BLUE),
                             lambda: [foot(t.get_value())[0], AX_Y - 0.75, 0], self.op_xl)
            self.add(self.xl)
            self.play(self.op_xl.animate.set_value(1.0), run_time=1.0)

            c.wait_until("put the weight")
            self.op_sp = ValueTracker(0.0)
            self.sp = faded(ak.spring_on_axis(t), self.op_sp)
            self.add(self.sp)
            self.play(self.op_sp.animate.set_value(1.0), run_time=1.5)
            c.wait_until("move as one")
            kit.legend_change(self, self.leg, "x", "the shadow", run_time=1.2)

            q1 = T("why should the shadow", size=32, color=YELLOW)
            q2 = T("obey the rule?", size=32, color=YELLOW)
            self.q = VGroup(q1, q2).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
            at_col(self.q, -2.6)
            c.wait_until("why should", own_word=q1)
            self.play(*appear(self.q), run_time=1.0)

    # ── c2.shadow.2: each part on its own, the shadow of the acceleration ───────────
    def clip2(self):
        t = self.t
        with self.say("c2.shadow.2") as c:
            # the tip's motion splits: BLUE on Re (already there), PINK on Im
            op_pk = ValueTracker(0.0)

            def pink():
                p = tip(t.get_value())
                q = ak.plane_point(1j * ph(t.get_value()).imag)
                ln = (DashedLine(p, q, dash_length=0.08).set_stroke(DIM, 2)
                      if np.linalg.norm(p - q) > 0.05 else VMobject())
                d = Dot(q, radius=0.09, color=PINK).set_z_index(-1.7)
                return VGroup(ln, d)
            pk = live(pink, op_pk)
            self.add(pk)
            du = MathTex(r"\frac{d}{dt}", font_size=32, color=BLUE).move_to([-0.8, 0.85, 0])
            dv = MathTex(r"\frac{d}{dt}", font_size=32, color=PINK).move_to([-3.8, 2.25, 0])
            for m in (du, dv):
                set_backstroke(m, width=5)
            self.play(op_pk.animate.set_value(1.0), FlashAround(Dot(foot(t.get_value()), radius=0.09),
                                                                 color=BLUE, time_width=1.5),
                      *appear(du, dv, shift=None, lag=0.3), run_time=1.5)
            c.wait_until("differentiating")
            split = tex([r"\frac{d}{dt}", "(", "u", "+", "i", "v", ")", "=", r"\dot{u}", "+", "i",
                         r"\dot{v}"], {2: BLUE, 5: PINK, 8: BLUE, 11: PINK})
            at_col(split, 1.5)
            self.play(*appear(split), run_time=1.5)
            each = kit.tag("each part on its own")
            at_col(each, 0.92)
            self.split, self.each = split, each
            c.wait_until("on its own")
            self.play(*appear(each, shift=None), run_time=1.0)

            # the acceleration at the tip (¼ scale) and its shadow
            c.wait_until("acc")
            self.play(op_pk.animate.set_value(0.0), *disappear(du, dv), run_time=0.8)
            self.remove(pk)
            self.op_ra = ValueTracker(0.0)

            def red_tip():
                p = ph(t.get_value())
                d = np.array([p.real, p.imag, 0.0])
                n = 0.13 * np.array([-d[1], d[0], 0.0])
                return ak.arrow_between(tip(t.get_value()) + n, O + n + 0.02 * d, RED, 6, -1.8)
            self.ra = live(red_tip, self.op_ra)
            self.add(self.ra)
            self.note = kit.tag("¼ scale").move_to([-0.95, -1.3, 0])
            set_backstroke(self.note, width=5)
            self.play(self.op_ra.animate.set_value(1.0), *appear(self.note, shift=None),  # early: a scale note
                      run_time=1.2)
            c.wait_until("acceleration of the shadow")
            self.op_rs = ValueTracker(0.0)
            self.rs = live(lambda: harrow(foot(t.get_value()), [O[0], AX_Y, 0], RED), self.op_rs)
            self.add(self.rs)
            rx = readout(r"x =", lambda: math.cos(OMEGA * t.get_value()), BLUE, [COL_X, -2.95, 0])
            rxx = readout(r"\ddot{x} =", lambda: -OMEGA ** 2 * math.cos(OMEGA * t.get_value()), RED,
                          [COL_X + 2.4, -2.95, 0])
            self.op_rd = ValueTracker(0.0)
            self.reads = [faded(rx, self.op_rd), faded(rxx, self.op_rd)]
            self.add(*self.reads)
            self.play(self.op_rs.animate.set_value(1.0),
                      *during(disappear(self.q), 0, 0.45), *during([self.op_rd.animate.set_value(1.0)], 0.5, 1),
                      run_time=1.4)

            # the arrow obeys; take the shadow of both sides; swap Re and d²/dt²
            c.wait_until("pull")
            self.L1 = tex([r"\frac{d^2}{dt^2}", r"e^{i\omega t}", "=", r"-\omega^2", r"e^{i\omega t}"],
                          {0: RED, 1: GOLD, 4: GOLD})
            at_col(self.L1, 0.3)
            self.play(*appear(self.L1), run_time=1.2)
            self.obeys = kit.tag("the arrow obeys", self.L1, RIGHT)
            c.wait_until("times the arrow", own_word=self.obeys)
            self.play(*appear(self.obeys, shift=None), run_time=0.8)
            c.wait_until("so its shadow")
            self.L2 = tex([r"\mathrm{Re}", r"\Big[", r"\frac{d^2}{dt^2}", r"e^{i\omega t}", r"\Big]", "=",
                           r"-\omega^2\,", r"\mathrm{Re}\,", r"e^{i\omega t}"],
                          {0: BLUE, 1: BLUE, 4: BLUE, 2: RED, 3: GOLD, 7: BLUE, 8: GOLD})
            at_col(self.L2, -0.85)
            self.s2 = step_at("shadow of both sides", -0.24)
            self.play(*appear(self.s2, self.L2, shift=None, lag=0.4), run_time=1.3)
            c.wait_until("times the shadow")
            self.L3 = tex([r"\frac{d^2}{dt^2}\,", r"\mathrm{Re}\,", r"e^{i\omega t}", "=",
                           r"-\omega^2\,", r"\mathrm{Re}\,", r"e^{i\omega t}"],
                          {0: RED, 1: BLUE, 2: GOLD, 5: BLUE, 6: GOLD})
            at_col(self.L3, -2.0)
            self.s3 = step_at("shadow of accel. = accel. of shadow", -1.45)
            self.play(*appear(self.s3, self.L3, shift=None, lag=0.4), run_time=1.3)

            # on the weight: the spring's pull
            c.wait_until("on the weight")
            lift = ValueTracker(0.0)
            self.op_pl = ValueTracker(1.0)
            dy = spr.BLOCK_H / 2 + spr.PULL_DY

            def pull():
                f = foot(t.get_value())
                y = AX_Y + lift.get_value() * dy
                return harrow([f[0], y, 0], [O[0], y, 0], RED, 2)
            self.pull = live(pull, self.op_pl)
            self.add(self.pull)
            self.play(lift.animate.set_value(1.0), run_time=1.5)
            c.wait_until("obeys")
            self.ctag = kit.corner_tag()
            self.play(FlashAround(self.pin.formula, color=YELLOW, time_width=1.5),
                      FlashAround(self.L3, color=YELLOW, time_width=1.5),
                      *appear(self.ctag, shift=None), run_time=1.6)  # early: tag on the new topic

    # ── c2.shadow.3: the shadow is cos ωt; it unrolls into s1's wave; the check ─────
    def clip3(self):
        t = self.t
        with self.say("c2.shadow.3") as c:
            # the derivation is done: the column and the RED arrows go, the clock freezes at 60°
            ak.run(t, False)
            cur = t.get_value()
            t1 = (PI / 6) + math.ceil((cur + 1.2 - PI / 6) / PI) * PI
            dt = t1 - cur
            self.op_leg = ValueTracker(0.0)
            self.legline = live(lambda: Line(O, foot(t.get_value()) + 1e-3 * RIGHT)
                                .set_stroke(BLUE, 7).set_z_index(-1.75), self.op_leg)
            self.op_cl = ValueTracker(0.0)
            self.cl = follow(MathTex(r"\cos\omega t", font_size=34, color=BLUE),
                             lambda: [(O[0] + foot(t.get_value())[0]) / 2, AX_Y - 0.32, 0], self.op_cl)
            self.add(self.legline, self.cl)
            fades = [m.animate.set_value(0.0) for m in (self.op_ra, self.op_rs, self.op_pl, self.op_sp,
                                                        self.op_xl)]
            f = min(0.45, 1.0 / dt)
            self.play(t.animate.set_value(t1), *during(disappear(self.note) + fades, 0, f),
                      *during([self.op_leg.animate.set_value(1.0), self.op_cl.animate.set_value(1.0)],
                              min(0.6, 1.1 / dt), 1.0),
                      rate_func=linear, run_time=dt)
            self.remove(self.ra, self.rs, self.pull, self.sp, self.xl)
            self.cap = tex(["x", "=", r"\mathrm{Re}\,", r"e^{i\omega t}", "=", r"\cos\omega t"],
                           {0: BLUE, 2: BLUE, 3: GOLD, 5: BLUE}, size=36)
            at_col(self.cap, 1.5)
            c.wait_until("cosine")
            outs = disappear(self.split, self.each, self.L1, self.obeys, self.s2, self.L2, self.s3,
                             self.L3) + [self.op_rd.animate.set_value(0.0)]
            self.play(*during(outs, 0, 0.45), *during(appear(self.cap), 0.5, 1.0), run_time=1.8)
            self.remove(*self.reads)

            # time runs down the screen: the shadow unrolls
            c.wait_until("unroll")
            top = np.array([O[0], AX_Y, 0])
            bot = np.array([O[0], AX_Y - hook.WAVE_SEC * UNROLL_T - 0.05, 0])
            self.tax = Arrow(top, bot, buff=0, stroke_width=3, tip_length=0.18,
                             max_tip_length_to_length_ratio=0.1, color=DIM)
            self.tlab = MathTex("t", font_size=32, color=DIM).move_to(bot + [0.28, 0.12, 0])
            self.xq = MathTex(r"x(t)", r"=\,?", font_size=48, color=YELLOW)
            at_col(self.xq, 0.5)
            self.play(*set_alpha([self.pl], 0.45), *appear(self.tax, self.tlab, shift=None),
                      self.op_cl.animate.set_value(0.0), *appear(self.xq), *disappear(self.fig),
                      run_time=0.9)
            self.remove(self.cl)

            def pen():
                tn = t.get_value()
                y = AX_Y - hook.WAVE_SEC * (tn - t1)
                xp = foot(tn)[0]
                curve = hook.hook_wave(top, tn, t1, color=BLUE, width=5)
                tie = (DashedLine([xp, AX_Y, 0], [xp, y, 0], dash_length=0.08).set_stroke(DIM, 2)
                       if AX_Y - y > 0.12 else VMobject())
                return VGroup(tie, curve, Dot([xp, y, 0], radius=0.075, color=BLUE))
            drawing = always_redraw(pen)
            self.add(drawing)
            self.play(t.animate.set_value(t1 + UNROLL_T), rate_func=linear, run_time=UNROLL_T)
            self.wave = hook.hook_wave(top, t1 + UNROLL_T, t1, color=BLUE, width=5).set_z_index(-1)
            self.remove(drawing)
            rest = pen()
            self.add(self.wave, rest[0], rest[2])
            # s1's wave (DIM), laid over: the two coincide
            self.s1wave = hook.hook_wave(top, t1 + UNROLL_T, t1, color=DIM, width=12)
            self.s1wave.set_stroke(DIM, 12, opacity=0.6).set_z_index(-1.5)
            self.s1wave.set_z_index(-1.2)
            self.wave.set_z_index(-1.1)
            print(f"S1WAVE_FADE_AT {self.time:.2f}", file=sys.stderr)
            self.play(FadeIn(self.s1wave), FadeOut(rest[0]), FadeOut(rest[2]), run_time=1.2)

            c.wait_until("cosine", nth=1)
            self.xa = MathTex(r"x(t)", "=", r"\cos\omega t", font_size=48, color=YELLOW)
            self.xa[2].set_color(BLUE)
            at_col(self.xa, 0.5)
            self.play(*edit(self.xq, self.xa), run_time=1.5)

            # read it back
            rb1 = T("cos ωt = the shadow of a point", size=28, color=YELLOW)
            rb2 = T("going round at ω rad/s", size=28, color=YELLOW)
            self.rb = VGroup(rb1, rb2).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
            at_col(self.rb, -0.55)
            c.wait_until("is the shadow", own_word=rb1)
            self.play(*appear(rb1), run_time=1.0)
            c.wait_until("going round", own_word=rb2)
            self.play(*appear(rb2), run_time=1.0)

            # the check (reference)
            c.wait_until("check")
            k1 = tex(["x", "=", r"\cos\omega t"], {0: BLUE, 2: BLUE})
            at_col(k1, -0.35)
            ref = kit.tag("reference", k1, RIGHT, buff=0.4)
            self.play(*during(disappear(self.cap, self.ctag), 0, 0.45),
                      *during([restyle(self.xa, op=0.4, shift=UP), rb1.animate.shift(UP),
                               rb2.animate.shift(UP)], 0.3, 1.0), run_time=1.4)
            self.play(*appear(k1, ref, shift=None, lag=0.3), run_time=1.0)  # early: the tier tag
            c.wait_until("two derivatives")
            k2 = tex([r"\dot{x}", "=", r"-\omega\sin\omega t"], {0: GREEN})
            at_col(k2, -1.05)
            s2 = step_at("chain rule", -0.7)
            k3 = tex([r"\ddot{x}", "=", r"-\omega^2\cos\omega t"], {0: RED})
            at_col(k3, -1.75)
            s3 = step_at("chain rule again", -1.4)
            self.play(*appear(s2, k2, shift=None, lag=0.4), run_time=min(1.2, c.until(floor=0.6)))
            self.play(*appear(s3, k3, shift=None, lag=0.4), run_time=min(1.2, c.until(floor=0.6)))
            k4 = tex(["=", r"-\omega^2", "x"], {2: BLUE})
            at_col(k4, -2.62)
            k4.shift((k3[1].get_center()[0] - k4[0].get_center()[0]) * RIGHT)
            s4 = step_at("cos ωt = x", -2.12)
            box = SurroundingRectangle(k4, color=YELLOW, buff=0.12).set_stroke(YELLOW, 3)
            self.play(*appear(s4, k4, shift=None, lag=0.4), GrowFromCenter(box),
                      run_time=min(1.3, c.until(floor=0.6)))
            self.check = [k1, ref, k2, s2, k3, s3, k4, s4, box]

    # ── c2.shadow.4: two different angles ───────────────────────────────────────────
    def clip4(self):
        t = self.t
        with self.say("c2.shadow.4") as c:
            self.op_pd = ValueTracker(0.0)

            def pend():
                th = -SWING * math.cos(OMEGA * t.get_value())
                g = grav.pendulum(th, labels=False, angle=False, pivot=PEND_P, length=PEND_L / PEND_S)
                g.scale(PEND_S, about_point=PEND_P)
                a = -th * DEGREES
                arc = Arc(radius=PEND_ARC_R, start_angle=-PI / 2, angle=a if abs(a) > 1e-3 else 1e-3,
                          arc_center=PEND_P).set_stroke(BLUE, 9)
                return VGroup(g, arc)
            self.pend = live(pend, self.op_pd)
            self.add(self.pend)
            ak.run(t, True)
            outs = disappear(self.tlab, self.tax, self.wave, self.s1wave)
            self.play(*during(outs, 0, 0.5), self.op_leg.animate.set_value(0.0),
                      *during(set_alpha([self.pl], 1.0), 0.3, 0.8),
                      *during([self.op_pd.animate.set_value(1.0)], 0.5, 1.0), run_time=1.6)
            self.remove(self.legline)

            # the arrow's angle grows forever
            c.wait_until("arrow_angle")
            self.play(*disappear(self.xa, *self.rb, *self.check), run_time=0.8)
            t.set_value(math.fmod(t.get_value(), PI))
            self.op_arc = ValueTracker(0.0)
            self.arc = faded(ak.angle_arc(t), self.op_arc)
            self.op_wt = ValueTracker(0.0)
            wt = ak.wt_readout(t, size=34)
            at_col(wt, 1.5)
            wt.add_updater(lambda m: m.set_opacity(self.op_wt.get_value()))
            wt.set_opacity(0)
            self.wt = wt
            self.add(self.arc, wt)
            self.play(self.op_arc.animate.set_value(1.0), self.op_wt.animate.set_value(1.0),
                      run_time=1.0)
            grows = T("ωt: grows forever", size=30, color=YELLOW)
            at_col(grows, 0.85)
            turns = kit.tag("2π ≈ 6.28    4π ≈ 12.57")
            at_col(turns, 0.38)
            c.wait_until("grows forever", own_word=grows)
            self.play(*appear(grows, turns, lag=0.3), run_time=1.2)

            # the pendulum's x stays small
            small = T("x: stays small", size=26, color=BLUE)
            small.move_to([-5.75, 2.62, 0], aligned_edge=LEFT)
            set_backstroke(small, width=5)
            c.wait_until("stays small", own_word=small)
            self.play(*appear(small), run_time=1.0)
            c.wait_until("it's the shadow")
            self.op_lk = ValueTracker(0.0)

            def link_line():
                th = -SWING * math.cos(OMEGA * t.get_value())
                a = -PI / 2 - th * DEGREES / 2
                s = PEND_P + PEND_ARC_R * np.array([math.cos(a), math.sin(a), 0])
                return DashedLine(s, foot(t.get_value()), dash_length=0.1).set_stroke(DIM, 2.5)
            self.link = live(link_line, self.op_lk)
            self.add(self.link)
            xs = T("x = the shadow", size=26, color=BLUE)
            xs.move_to([-5.75, 2.2, 0], aligned_edge=LEFT)
            set_backstroke(xs, width=5)
            self.play(self.op_lk.animate.set_value(1.0), *appear(xs), run_time=1.2)
            self.texts4 = [grows, turns, small, xs]

    # ── the handover shot: GOLD frozen at 50°, the block back on the axis, λ box ────
    def finish(self):
        t = self.t
        self.wait(2.0)
        ak.run(t, False)
        cur = t.get_value()
        target = T_HAND + math.ceil((cur - T_HAND) / PI + 1e-6) * PI
        dt = target - cur
        if dt < 1.0:
            target += PI
            dt += PI
        outs = disappear(*self.texts4) + [m.animate.set_value(0.0)
                                          for m in (self.op_pd, self.op_lk, self.op_arc, self.op_wt)]
        self.play(t.animate.set_value(target), *during(outs, 0, min(0.5, 1.0 / dt)),
                  rate_func=linear, run_time=dt)
        self.remove(self.pend, self.link, self.arc, self.wt)
        lam = ak.lambda_box()
        kit.col_place(lam, 0)
        self.op_sp.set_value(0.0)
        self.add(self.sp)
        self.play(self.op_sp.animate.set_value(1.0), *appear(lam), run_time=1.2)
        # swap the live drawings for the still shot (identical pixels)
        shot = handover_shot()
        self.remove(*[m for mob in (self.pl, self.gold, self.sh, self.sp, self.card, self.pin,
                                    self.leg, lam) for m in mob.get_family()])
        self.add(shot)
        self.wait(1.0)
