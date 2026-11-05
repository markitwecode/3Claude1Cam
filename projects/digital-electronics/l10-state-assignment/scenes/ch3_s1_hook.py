"""Chapter 3, scene 1: hook. ch2's end card, the title card, the ring of five switched on: the output
stays flat at 0. Clips c3.hook.1 – c3.hook.3.

Opens exactly on ch2_s8_recap's end card (ch2_end_card() below rebuilds it), then the title card.

Shared (s2 opens on handover_shot(); s6, s7, s8 reuse the pieces):
  ring_leds()     ch2_s6's ring_circuit() scaled to RL_W wide at RL_CENTER, an LED (GREEN ring dark,
                  filled GREEN lit) above each box, hooked to its own Q wire. VGroup(rc, *stubs, *leds); attrs .rc .stubs .leds
                  .ffs .clk_paths() (CLK bus + every clock pin, copies for VShowPassingFlash)
                  .pass_paths() (each Q -> next D, e's via the feedback, copies for flashes).
                  Change LEDs with set_led(led, on).
  wave_panel()    the waveform panel under it: labels "1 Hz" GOLD, "CLK" YELLOW, "output = b" GREEN
                  hanging left of W_X0; ten periods of W_P. Attrs .labels .clk_pieces[j] (one CLK
                  period each: .wave + its ▲) .out_pieces[j] (flat GREEN at 0, one per period)
                  .x(j) (x of rising edge j). Built complete; animate pieces with Create.
  ghost_wave()    the wanted output (high 2 periods, low 3, twice), dashed, faint GREEN.
  handover_shot() ring_leds() + wave_panel() complete (flat output); this scene's last frame.
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402


def _p(x, y):
    return np.array([x, y, 0.0])


_S6 = load_scene("ch2_s6_nologic")
BOX_W, PIN_Y, BOX_H_N = _S6.BOX_W, _S6.PIN_Y, _S6.BOX_H

# ---- ch2's last frame (ch2_s8_recap end card) ------------------------------------------------------
CH2_TRACE_Y = -3.3
CH2_TRACE_X = (-5.0, 6.0)


def ch2_end_card():
    rc = _S6.ring_circuit()
    out_l = T("output", 30, GREEN)
    out_l.move_to(_p(CH2_TRACE_X[0] - 0.25, CH2_TRACE_Y), aligned_edge=RIGHT)
    trace = Line(_p(CH2_TRACE_X[0], CH2_TRACE_Y), _p(CH2_TRACE_X[1], CH2_TRACE_Y)).set_stroke(GREEN, 4)
    q = T("?", 64, RED).move_to(_p(0.5, -2.75))
    part3 = T("Part 3 · Starting in a used state", 40).move_to(_p(0, 3.2))
    g = VGroup(rc, out_l, trace, q, part3)
    g.rc = rc
    return g


# ---- LEDs: one above each flip-flop's box, tapped off its own Q wire ---------------------------------
LED_R = 0.36        # native radius (x k = 0.62 on screen: r ~ 0.22)
LED_DX = 0.2        # native: LED centre right of the box centre (over the Q side)
LED_Y = 1.85        # native: LED centre height (box top 1.3, feedback 2.7)
TAP_DX = 0.9        # native: where the stub leaves the Q wire, right of the box centre


def _led_style(c, on):
    c.set_stroke(GREEN, 5).set_fill(GREEN, 0.95 if on else 0)
    return c


def led(on, r=LED_R):
    c = _led_style(Circle(radius=r), on)
    c.on = on
    return c


def set_led(l, on):
    l.on = on
    return _led_style(l.animate, on)


# ---- the ring with LEDs -----------------------------------------------------------------------------
RL_W = 10.2
RL_CENTER = _p(0.0, 1.38)


def ring_leds():
    """LEDs sit above their own flip-flop's box (never in the gap between two boxes), each wired by a
    small GREEN hook from a dot on its own Q wire; the topmost point stays well under the feedback."""
    rc = _S6.ring_circuit()
    rc.scale_to_fit_width(RL_W).move_to(RL_CENTER)
    k = rc.ffs[0].box.width / BOX_W
    stubs, leds = [], []
    for f in rc.ffs:
        bc = f.box.get_center()
        qy = f.q_w.get_center()[1]
        top = f.box.get_top()[1]
        c = _p(bc[0] + LED_DX * k, top + (LED_Y - BOX_H_N / 2) * k)
        tap = _p(bc[0] + TAP_DX * k, qy)
        path = VMobject().set_points_as_corners([tap, _p(tap[0], c[1]), c + LED_R * k * RIGHT])
        path.set_stroke(GREEN, 3)
        stubs.append(VGroup(path, Dot(tap, radius=0.05, color=GREEN)))
        leds.append(led(False, LED_R * k).move_to(c))
    g = VGroup(rc, *stubs, *leds)
    g.rc, g.stubs, g.leds, g.ffs = rc, stubs, leds, rc.ffs

    def clk_paths(width=9):
        return [m.copy().set_stroke(YELLOW, width) for m in [rc.clk] + [f.clk_w for f in rc.ffs]]

    def pass_paths(width=9):
        ffs = rc.ffs
        out = [Line(ffs[i].q_w.get_start(), ffs[i + 1].d_w.get_end()).set_stroke(GREEN, width)
               for i in range(4)]
        pts = [ffs[4].q_w.get_start(), *rc.feedback.get_anchors(), ffs[0].d_w.get_end()]
        out.append(VMobject().set_points_as_corners(pts).set_stroke(GREEN, width))
        return out

    g.clk_paths, g.pass_paths = clk_paths, pass_paths
    return g


# ---- the waveform panel -----------------------------------------------------------------------------
W_X0, W_P, W_N, W_H = -3.8, 0.96, 10, 0.6
W_CLK_Y, W_OUT_Y = -0.85, -2.05
W_LAB_X = -4.15


def clk_period(x, y, p=W_P, h=W_H, color=YELLOW, width=4):
    """One CLK period from x: rises at x, high for p/2, low for p/2, with a small ▲ on the rise."""
    lo, hi = y - h / 2, y + h / 2
    wave = VMobject().set_points_as_corners(
        [_p(x, lo), _p(x, hi), _p(x + p / 2, hi), _p(x + p / 2, lo), _p(x + p, lo)]).set_stroke(color, width)
    up = Triangle().scale(0.1).set_stroke(width=0).set_fill(color, 1).move_to(_p(x, y))
    g = VGroup(wave, up)
    g.wave, g.up = wave, up
    return g


def wave_panel():
    clk_l = T("CLK", 32, YELLOW).next_to(_p(W_LAB_X, W_CLK_Y), LEFT, buff=0)
    hz = T("1 Hz", 30, GOLD).next_to(clk_l, LEFT, buff=0.35)
    out_l = T("output = b", 32, GREEN).next_to(_p(W_LAB_X, W_OUT_Y), LEFT, buff=0)
    x = lambda j: W_X0 + j * W_P  # noqa: E731
    lo = W_OUT_Y - W_H / 2
    clk_pieces = [clk_period(x(j), W_CLK_Y) for j in range(W_N)]
    out_pieces = [Line(_p(x(j), lo), _p(x(j + 1), lo)).set_stroke(GREEN, 4) for j in range(W_N)]
    labels = VGroup(hz, clk_l, out_l)
    g = VGroup(labels, *clk_pieces, *out_pieces)
    g.labels, g.hz, g.clk_l, g.out_l = labels, hz, clk_l, out_l
    g.clk_pieces, g.out_pieces, g.x, g.lo = clk_pieces, out_pieces, x, lo
    return g


def ghost_wave(pattern=(1, 1, 0, 0, 0)):
    x = lambda j: W_X0 + j * W_P  # noqa: E731
    lev = lambda b: W_OUT_Y + (W_H / 2 if b else -W_H / 2)  # noqa: E731
    pts = []
    for j in range(W_N):
        b = pattern[j % 5]
        pts += [_p(x(j), lev(b)), _p(x(j + 1), lev(b))]
    path = VMobject().set_points_as_corners(pts)
    g = DashedVMobject(path, num_dashes=70, dashed_ratio=0.55).set_stroke(GREEN, 3, opacity=0.4)
    return g


def handover_shot():
    return VGroup(ring_leds(), wave_panel())


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        # handover: the shot s2 opens on, held
        self.play(*during(disappear(self.q, self.start_l, self.ghost, self.tag), 0.4, 1), *self.ticks(1.2), run_time=1.2)
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(1.0)

    def ticks(self, rt, period=1.2, t0=0.0):
        out, t = [], t0
        while t + 0.8 <= rt + 1e-6:
            out += [time_span(VShowPassingFlash(m, time_width=0.6), t, t + 0.8) for m in self.rl.clk_paths()]
            t += period
        return out

    # -- c3.hook.1: ch2's end card -> title card -> the ring of five ----------------------------------
    def clip1(self):
        end = ch2_end_card()
        self.add(*end)
        self.rl = ring_leds()
        with self.say("c3.hook.1") as c:
            card = title_card("Part 3 · Starting in a used state")
            if card.title.width > 12.0:
                card.title.scale_to_fit_width(12.0)
            part3 = end[4]
            self.wait(0.7)   # ch2's end card holds a moment: the cut reads as a continuation
            rest = [m for m in end if m is not part3]
            self.play(*during(disappear(*rest), 0, 0.4),
                      *during([part3.animate.scale(card.part.height / part3.height).move_to(card.part)], 0.1, 0.6),
                      *during(appear(card.title, card.rule, card.course, lag=0.2), 0.55, 1),  # early: title card
                      run_time=min(2.0, c.until("ring")))
            self.remove(part3)
            self.add(card.part)

            c.wait_until("ring")
            sweep_clear(self, FadeIn(self.rl.rc), run_time=1.4)  # early: ch2's circuit, shown whole

            c.wait_until("flip-flops")
            tag = self.tag = T("ring · 5 flip-flops · no gates", 30, t2c={"5": GOLD}).move_to(_p(0, 3.3))
            self.play(*appear(tag), run_time=1.0)

            # every edge: the clock pulses, then each bit passes along its wire
            c.wait_until("every edge")
            self.play(*self.ticks(1.0), run_time=1.0)
            c.wait_until("passes")
            self.play(*[VShowPassingFlash(m, time_width=0.5) for m in self.rl.pass_paths()],
                      run_time=min(1.6, c.until(floor=0.8)))

    # -- c3.hook.2: switched on; the output stays flat; the wanted wave as a ghost --------------------
    def clip2(self):
        rl = self.rl
        pn = self.pn = wave_panel()
        ghost = self.ghost = ghost_wave()
        with self.say("c3.hook.2") as c:
            self.play(*appear(*rl.stubs, *rl.leds, lag=0.08, shift=None),  # early: the panel's axes
                      *during(appear(*pn.labels, lag=0.25, shift=None), 0.3, 1),
                      run_time=1.4)
            per = max(0.7, c.until("instead") / W_N)
            t_flat, t_ghost = c.at("flat"), c.at("ghost")
            done = set()
            for j in range(W_N):
                cp, op = pn.clk_pieces[j], pn.out_pieces[j]
                anims = [Create(cp.wave, rate_func=linear), FadeIn(cp.up, scale=0.5),
                         Create(op, rate_func=linear),
                         *[time_span(VShowPassingFlash(m, time_width=0.6), 0, min(0.8, per))
                           for m in rl.clk_paths()]]
                if "flat" not in done and self.time + per > t_flat:
                    done.add("flat")
                    run = Line(_p(W_X0, pn.lo), _p(pn.x(j + 1), pn.lo)).set_stroke(GREEN, 9)
                    anims.append(VShowPassingFlash(run, time_width=0.6))
                if "ghost" not in done and self.time + per > t_ghost:
                    done.add("ghost")
                    anims.append(FadeIn(ghost))
                self.play(*anims, run_time=per)
            if "ghost" not in done:
                self.play(FadeIn(ghost), run_time=0.8)

    # -- c3.hook.3: why? where does a machine start? ----------------------------------------------------
    def clip3(self):
        pn = self.pn
        with self.say("c3.hook.3") as c:
            q = self.q = T("?", 64, RED).move_to(_p(pn.x(3.5), pn.lo + 0.62))
            self.play(*appear(q, shift=None), *self.ticks(1.2), run_time=1.2)
            c.wait_until("does it do nothing")
            self.play(FlashAround(q, color=RED, time_width=1.5), q.animate(rate_func=there_and_back).scale(1.25),
                      *self.ticks(1.2), run_time=1.2)
            c.wait_until("start")
            sl = self.start_l = T("where does a machine start?", 34).move_to(_p(0, -3.2))
            self.play(*appear(sl), *self.ticks(1.2), run_time=1.2)
            while c.remaining > 1.3:
                self.play(*self.ticks(1.2), run_time=1.2)
            c.wait_until()
