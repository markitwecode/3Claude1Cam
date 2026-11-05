"""Chapter 2, scene 6: two arrows, one swing (e^{-iωt} the mirror; tip to tail the sum rides the real axis at 2cos ωt). Clips c2.mirror.1 – c2.mirror.3.

Shared: mirror_pair(t, scale=1, origin=ak.PLANE_O, carry=1, legs=0, total=0, chord=0, purple=1)
draws GOLD e^{iωt} and PURPLE e^{-iωt}; `carry` 0 = PURPLE from the origin, 1 = tip to tail on GOLD;
`legs` the two PINK vertical parts (up on GOLD, down on PURPLE); `total` the BLUE dot at the chain's
end (2cos ωt); `chord` the DIM segment GOLD tip – PURPLE tip with the BLUE midpoint (= the shadow).
Every argument but scale/origin may be a number (still) or a ValueTracker (live, redrawn each frame).
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
s5 = load_scene("ch2_s5_shadow")

OMEGA = ak.OMEGA
T_HAND = s5.T_HAND                      # GOLD at 50°, PURPLE at -50°
E_MIRROR = (r"e^{-i\omega t}", PURPLE, "mirror arrow")
ENTRIES6 = [s5.E_X_SHADOW, kit.E_XDD, ak.E_W, ak.E_T, ak.E_LAM, ak.E_ARROW, E_MIRROR, ak.E_ANGLE]   # velocity out, the mirror in column 2
CS = 34


def _v(x):
    return x.get_value() if hasattr(x, "get_value") else float(x)


def _op(m, a):
    if a < 0.999:
        s5._opacify(m, max(a, 0.0))
    return m


def mirror_pair(t, scale=1.0, origin=ak.PLANE_O, carry=1.0, legs=0.0, total=0.0, chord=0.0,
                purple=1.0, width=6):
    """GOLD e^{iωt} and PURPLE e^{-iωt} (see the module docstring)."""
    o = np.array(origin, dtype=float)

    def P(z):
        return ak.plane_point(z, scale, o)

    def build():
        tv = _v(t)
        g = ak.phasor(tv)
        p = ak.phasor(tv, -OMEGA)
        base = _v(carry) * g
        parts = [ak.arrow_between(o, P(g), GOLD, width, -2)]
        pu = _v(purple)
        if pu > 0.001:
            parts.append(_op(ak.arrow_between(P(base), P(base + p), PURPLE, width, -1.95), pu))
        lg = _v(legs)
        if lg > 0.001:
            if abs(g.imag) * ak.PLANE_R * scale > 0.12:
                up = ak.arrow_between(P(g.real), P(g), PINK, 5, -1.85)
                dn_top = complex(base.real + p.real, base.imag)
                dn = ak.arrow_between(P(dn_top), P(base + p), PINK, 5, -1.85)
                parts += [_op(up, lg), _op(dn, lg)]
        ch = _v(chord)
        if ch > 0.001:
            seg = Line(P(g), P(base + p)).set_stroke(DIM, 3).set_z_index(-1.9)
            mid = Dot(P((g + base + p) / 2), radius=0.1, color=BLUE).set_z_index(-1.7)
            parts += [_op(seg, ch), _op(mid, ch)]
        tt = _v(total)
        if tt > 0.001:
            parts.append(_op(Dot(P(base + p), radius=0.11, color=BLUE).set_z_index(-1.7), tt))
        return VGroup(*parts)

    return ak._dyn(build, t, carry, legs, total, chord, purple)


def ring_pulse(point_fn, color=BLUE, run_time=1.4):
    """An expanding ring that follows a moving point and fades (a flash for a moving dot)."""
    ring = Circle(radius=0.12).set_stroke(color, 5)

    def upd(m, a):
        m.become(Circle(radius=0.12 + 0.4 * a).set_stroke(color, 5, opacity=1 - a).move_to(point_fn()))
    return UpdateFromAlphaFunc(ring, upd, run_time=run_time, remover=True)


def tex(parts, colors, size=CS):
    m = MathTex(*parts, font_size=size)
    for i, col in colors.items():
        m[i].set_color(col)
    return m


class Mirror(NarratedScene):
    def construct(self):
        # the handover shot from s5, then its moving parts swapped for live ones (same pixels)
        shot = s5.handover_shot()
        self.add(shot)
        self.t = ak.clock(ValueTracker(T_HAND))
        self.add(self.t)
        t = self.t
        self.remove(shot)
        self.pl, self.card, self.pin, self.leg, self.lam = shot.plane, shot.card, shot.pin, shot.legend, shot.lam
        self.op_pu, self.carry = ValueTracker(0.0), ValueTracker(0.0)
        self.op_legs, self.op_tot, self.op_ch = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.pair = mirror_pair(t, carry=self.carry, legs=self.op_legs, total=self.op_tot,
                                chord=self.op_ch, purple=self.op_pu)
        self.op_sh, self.op_sp = ValueTracker(1.0), ValueTracker(1.0)
        self.sh = s5.faded(ak.shadow(t), self.op_sh)
        self.sp = s5.faded(ak.spring_on_axis(t), self.op_sp)
        self.add(self.pl, self.sp, self.pair, self.sh, self.card, self.pin, self.leg, self.lam)
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(2.0)          # it stays true as they turn
        ak.run(t, False)
        for m in self.mobjects:
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects if not isinstance(m, ValueTracker)], run_time=1.0)
        self.wait(0.15)

    # ── c2.mirror.1: the other λ, the mirror arrow, it obeys the rule, same shadow ──────
    def clip1(self):
        t = self.t
        with self.say("c2.mirror.1") as c:
            self.play(FlashAround(self.lam, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("minus")
            self.play(*recolor(self.lam.line[2], PURPLE), FlashAround(self.lam.line[2], color=PURPLE),
                      run_time=1.2)

            # the mirror arrow grows out of the GOLD one by reflection in the real axis
            c.wait_until("purple")
            src = ak.turning_arrow(T_HAND)
            dst = ak.turning_arrow(T_HAND, omega=-OMEGA, color=PURPLE, z=-1.95)
            self.play(ReplacementTransform(src, dst), run_time=1.6)
            self.remove(dst)
            self.op_pu.set_value(1.0)
            c.wait_until("mirror")
            # every row shifts (a wider symbol column): a cross-fade instead of legend_set's slide
            new_leg = kit.legend(ENTRIES6, ak.LEG_ROWS)
            self.play(*during(disappear(self.leg), 0, 0.45), *during(appear(new_leg, shift=None), 0.5, 1.0),  # early: the standing legend, re-laid out
                      run_time=1.2)
            self.leg = new_leg

            c.wait_until("turning clockwise")
            self.op_arc = ValueTracker(0.0)
            self.arc = s5.faded(ak.angle_arc(t, omega=-OMEGA, color=PURPLE), self.op_arc)
            self.add(self.arc)
            ak.run(t, True)
            self.play(self.op_arc.animate.set_value(1.0), run_time=1.0)

            # it obeys the rule too
            c.wait_until("obeys")
            self.s1 = s5.step_at("i² = −1", 1.0)
            self.l1 = tex(["(", r"-i\omega", ")^2", "=", r"-\omega^2"], {1: PURPLE})
            self.l1[1][1].set_color(PINK)
            s5.at_col(self.l1, 0.55)
            self.play(*appear(self.s1, self.l1, shift=None, lag=0.4), run_time=1.4)
            self.s2 = s5.step_at("each d/dt brings −iω", 0.05)
            self.l2 = tex([r"\frac{d^2}{dt^2}", r"e^{-i\omega t}", "=", r"-\omega^2", r"e^{-i\omega t}"],
                          {0: RED, 1: PURPLE, 4: PURPLE})
            s5.at_col(self.l2, -0.55)
            self.ok = check_mark().scale(0.8).next_to(self.l2, RIGHT, buff=0.35)
            c.wait_until("obeys the rule")
            self.play(*appear(self.s2, self.l2, shift=None, lag=0.4), run_time=1.4)
            self.play(*appear(self.ok, shift=None), run_time=0.8)

            # same shadow: both drop lines meet at the one BLUE dot
            c.wait_until("same")
            self.op_psh = ValueTracker(0.0)
            self.psh = s5.faded(ak.shadow(t, omega=-OMEGA), self.op_psh)
            self.add(self.psh)
            self.play(self.op_psh.animate.set_value(1.0), run_time=1.2)
            c.wait_until("mirror in the real axis")
            self.play(ring_pulse(lambda: ak.plane_point(ak.phasor(t.get_value()).real)), run_time=1.4)

    # ── c2.mirror.2: tip to tail, the up and down parts cancel, the sum rides the axis ──
    def clip2(self):
        t = self.t
        with self.say("c2.mirror.2") as c:
            # decelerate to a freeze at GOLD 50° just after {predict}: r(a) = 1 - (1-a)^p starts at
            # the clock's speed when p = R / dt
            ak.run(t, False)
            start = self.time
            R = c.at("predict") + 0.4 - start
            cur = t.get_value()
            best = None
            for k in range(0, 8):
                target = T_HAND + (math.ceil((cur - T_HAND) / PI) + k) * PI
                dt = target - cur
                if dt <= 0.05:
                    continue
                p = R / dt
                if best is None or abs(math.log(p / 2.0)) < abs(math.log(best[1] / 2.0)):
                    best = (target, p)
            target, p = best
            p = max(p, 1.0)

            self.pair_tag = VGroup(kit.tag("the De Moivre video's picture,"), kit.tag("now moving in time"))
            self.pair_tag.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            s5.at_col(self.pair_tag, -1.6)
            self.ctag = kit.corner_tag()
            f1 = min(1.2 / R, 0.4)
            fm = (c.at("now they move") - start) / R
            fm = min(max(fm, f1 + 0.02), 0.85)
            self.play(t.animate(rate_func=lambda a: 1 - (1 - a) ** p).set_value(target),
                      *during(appear(self.pair_tag[0], shift=None), 0, f1),
                      *during(set_alpha([self.s1, self.l1, self.s2, self.l2, self.ok], 0.4), 0, f1),
                      *during([self.op_sp.animate.set_value(0.0)], 0, f1),
                      *during(appear(self.pair_tag[1], self.ctag, shift=None), fm, min(fm + 1.0 / R, 1.0)),
                      run_time=R)
            self.remove(self.sp)

            # carry PURPLE to the GOLD tip
            outs = [self.op_arc.animate.set_value(0.0), self.op_sh.animate.set_value(0.0),
                    self.op_psh.animate.set_value(0.0)]
            self.play(*during(outs, 0, 0.35), *during([self.carry.animate.set_value(1.0)], 0.25, 1.0),
                      run_time=min(1.8, c.until("what do you expect", floor=1.0)))
            self.remove(self.arc, self.sh, self.psh)

            # the question: what do the up and down parts do?
            g = ak.phasor(T_HAND)
            self.q = MathTex("?", font_size=64, color=YELLOW)
            self.q.move_to(ak.plane_point(complex(1.5 * g.real, g.imag)) + 0.45 * UP)
            c.wait_until("up and down")
            self.play(self.op_legs.animate.set_value(1.0), *during(appear(self.q), 0.3, 1.0), run_time=1.3)

            # they cancel: the two legs flash, slide together and vanish (the originals stay)
            c.wait_until("cancel")
            up_g = ak.arrow_between(ak.plane_point(g.real), ak.plane_point(g), PINK, 5, -1.8)
            dn_g = ak.arrow_between(ak.plane_point(complex(2 * g.real, g.imag)), ak.plane_point(2 * g.real),
                                    PINK, 5, -1.8)
            dx = (dn_g.get_center()[0] - up_g.get_center()[0]) / 2
            print(f"CANCEL_PLAY_AT {self.time:.2f}", file=sys.stderr)
            self.play(*during(flash([up_g, dn_g], color=PINK), 0, 0.5),
                      *during([up_g.animate.shift(dx * RIGHT).set_opacity(0),
                               dn_g.animate.shift(dx * LEFT).set_opacity(0)], 0.4, 1.0),
                      run_time=2.0)
            self.remove(up_g, dn_g)

            # one rises as the other falls: release
            c.wait_until("one rises")
            ak.run(t, True)
            self.play(*disappear(self.q), run_time=0.8)

            # the sum rides the real axis at 2cos ωt
            c.wait_until("ride")
            self.op_ro = ValueTracker(0.0)
            self.ro = s5.faded(s5.readout(r"2\cos\omega t =", lambda: 2 * math.cos(OMEGA * t.get_value()),
                                          BLUE, [kit.COL_LEFT, -3.05, 0], size=40), self.op_ro)
            self.add(self.ro)
            self.play(self.op_legs.animate.set_value(0.0), self.op_tot.animate.set_value(1.0),
                      *during(disappear(self.s1, self.l1, self.s2, self.l2, self.ok, self.pair_tag), 0, 0.5),
                      *during([self.op_ro.animate.set_value(1.0)], 0.4, 1.0), run_time=1.4)
            self.la = tex([r"e^{i\omega t}", "+", r"e^{-i\omega t}", "=", r"2\cos\omega t"],
                          {0: GOLD, 2: PURPLE, 4: BLUE}, size=38)
            s5.at_col(self.la, 0.75)
            c.wait_until("two times")
            self.play(*appear(self.la, shift=None), run_time=1.2)

    # ── c2.mirror.3: the caption, read back, average = shadow ───────────────────────
    def clip3(self):
        t = self.t
        with self.say("c2.mirror.3") as c:
            self.sd = s5.step_at("divide by two", 0.22)
            self.cap = tex([r"\cos\omega t", "=", r"\tfrac{1}{2}\big(", r"e^{i\omega t}", "+",
                            r"e^{-i\omega t}", r"\big)"], {0: BLUE, 3: GOLD, 5: PURPLE}, size=46)
            s5.at_col(self.cap, -0.35)
            self.box = SurroundingRectangle(self.cap, color=YELLOW, buff=0.14).set_stroke(YELLOW, 3)
            self.play(*appear(self.sd, self.cap, shift=None, lag=0.4), run_time=1.5)
            self.ref = kit.tag("(77) · notes p. 102")
            self.ref.next_to(self.box, DOWN, buff=0.15).align_to(self.box, RIGHT)
            c.wait_until("cosine")
            self.play(GrowFromCenter(self.box), *appear(self.ref, shift=None), run_time=1.2)

            rb = VGroup(T("a real swing", size=30, color=YELLOW),
                        T("= two complex swings,", size=30, color=YELLOW),
                        T("turning opposite ways", size=30, color=YELLOW))
            rb.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            s5.at_col(rb, -1.82)
            c.wait_until("read")
            for line in rb:
                c.wait_until(own_word=line)
                self.play(*appear(line, shift=None), run_time=0.9)

            # both arrows back at the origin: the midpoint of their tips is the shadow
            c.wait_until("average")
            self.avg = T("average = shadow", size=34, color=BLUE)
            s5.at_col(self.avg, -3.05)
            self.play(self.carry.animate.set_value(0.0), self.op_tot.animate.set_value(0.0),
                      *during([self.op_ch.animate.set_value(1.0)], 0.4, 1.0),
                      *during([self.op_ro.animate.set_value(0.0)], 0, 0.4),
                      *during(appear(self.avg, shift=None), 0.5, 1.0), run_time=1.8)
            self.remove(self.ro)
