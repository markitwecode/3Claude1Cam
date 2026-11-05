"""Chapter 3, scene 7: into a used state. Clips c3.restart.1 – c3.restart.3.

Opens on ch3_s6_preset's handover_shot() (ring, clock source, open switch, dark LEDs, "state 00000",
S pins + push buttons on d and e). d then e are set by hand (GOLD 1s under them, readout 11000, a
used state, ch2's table row lit); the ring moves up to s1's place, the clock is reconnected and s1's
waveform panel draws output b onto the ghost wave. Two lessons; then the start-up pulse: a power
switch, one RED line to S of d, e and R of a, b, c; three power-ups land on 11000.
"""
# style: 2
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

S6 = load_scene("ch3_s6_preset")
S1 = load_scene("ch3_s1_hook")
S5 = load_scene("ch2_s5_ring")
set_led = S1.set_led
press, flip = S6.press, S6.flip
BOX_W = S6.BOX_W
BUB_R = S6.BUB_R
UP_DY = S6.RING_DY          # the ring goes back up to s1's place for the waveform
PANEL_DY = 0.6              # s1's waveform panel, lowered to clear the ring's tokens
TAB_S, TAB_C = 0.7, (-3.0, -2.3)    # ch2's table, titles dropped, rows tightened: digits ~25
BUS_Y = -0.45               # start-up pulse bus under the ring (after the move up)
RISER_X = 5.75
TOK_SIZE = 38


def _p(x, y):
    return np.array([x, y, 0.0])


def pin_pulse(pins):
    """A colour pulse on async pins: the wire flashes, the S/R letter swells YELLOW and settles back RED."""
    out = []
    for p in pins:
        out.append(VShowPassingFlash(p.wire.copy().set_stroke(YELLOW, 10), time_width=0.8))
        out.append(p.label.animate(rate_func=there_and_back).set_color(YELLOW).scale(1.35))
    return out


class Restart(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---- helpers ------------------------------------------------------------------------------
    def tok_pos(self, i):
        return _p(self.ffs[i].box.get_x(), self.rc.clk.get_y() - 0.48)

    def new_tok(self, i):
        return value_label("1", TOK_SIZE, GOLD).move_to(self.tok_pos(i))

    def readout_to(self, s):
        new = Mono(s, 44, FG).move_to(self.digits)
        anims = swap(self.digits, new)
        self.digits = new
        return anims

    def leds_to(self, bits):
        out = []
        for led, b in zip(self.leds, bits):
            if bool(led.on) != bool(b):
                out.append(set_led(led, bool(b)))
        return out

    # -- c3.restart.1: set d, then e, by hand: 11000, a used state --------------------------------
    def clip1(self):
        sh = S6.handover_shot()
        self.sh = sh
        self.rl, self.rc = sh.rl, sh.rc
        self.ffs, self.leds = sh.rc.ffs, sh.rl.leds
        self.src, self.lead, self.sw, self.link = sh.src, sh.lead, sh.sw, sh.link
        self.lab, self.digits = sh.readout[0], sh.readout[1]
        pd, bd, pe, be = sh.extras
        self.pins_s, self.btns = [pd, pe], [bd, be]
        self.add(self.rl, self.src, self.lead, self.sw, self.link, self.lab, self.digits, *sh.extras)
        rl = self.rl
        self.tokens = {}

        with self.say("c3.restart.1") as c:
            # d: press, S = 0, Q = 1, release
            self.play(press(bd), FlashAround(bd, time_width=1.5), run_time=min(1.2, c.until("set went")))
            settle(self, bd)
            c.wait_until("set went to zero")
            lv_d = value_label("0", 34, RED).next_to(pd.label, LEFT, buff=0.2)
            self.play(*appear(lv_d), run_time=0.8)
            c.wait_until("cue went to one")
            tok_d = self.new_tok(3)
            self.tokens[3] = tok_d
            self.play(set_led(self.leds[3], True), FlashAround(self.leds[3], color=GREEN, time_width=1.5),
                      *during(appear(tok_d), 0.3, 1), *self.readout_to("01000"), run_time=1.4)
            settle(self, rl)
            c.wait_until("then he let")
            lv_d1 = value_label("1", 34, RED).move_to(lv_d)
            self.play(press(bd, False), *swap(lv_d, lv_d1), run_time=1.1)
            settle(self, bd)

            # e: the same, quicker
            c.wait_until("sete")
            lv_e = value_label("0", 34, RED).next_to(pe.label, LEFT, buff=0.2)
            self.play(press(be), *appear(lv_e), run_time=0.9)
            settle(self, be)
            tok_e = self.new_tok(4)
            self.tokens[4] = tok_e
            self.play(set_led(self.leds[4], True), *during(appear(tok_e), 0.2, 1),
                      *self.readout_to("11000"), run_time=1.1)
            settle(self, rl)
            lv_e1 = value_label("1", 34, RED).move_to(lv_e)
            self.play(press(be, False), *swap(lv_e, lv_e1), run_time=min(1.0, c.until("used", floor=0.6)))
            settle(self, be)

            # two ones side by side
            c.wait_until("used")
            self.play(*flash([tok_d, tok_e], color=GOLD, time_width=1.5),
                      *flash([self.leds[3], self.leds[4]], color=GREEN, time_width=1.5), run_time=1.5)
            c.wait_until("one one zero")

            # the corner table: row 11000 -> 10001
            tab = S5.ring_table()
            tab.remove(tab.titles)
            hy = tab.hline.get_y() + 0.42
            for k in range(5):
                for d in tab.cur[k] + tab.nxt[k]:
                    d.set_y(hy - 0.85 - 0.55 * k)
                    if k != 3:
                        d.set_opacity(0.4)
            vx = tab.vline.get_x()
            tab.vline.put_start_and_end_on(_p(vx, hy + 0.3), _p(vx, hy - 0.85 - 2.2 - 0.25))
            tab.scale(TAB_S).move_to(_p(*TAB_C))
            row = VGroup(*[d.copy() for d in tab.cur[3] + tab.nxt[3]])
            rowbox = SurroundingRectangle(row, color=GREEN, buff=0.05).set_stroke(GREEN, 3)
            self.tab, self.rowbox = tab, rowbox
            self.play(*during(disappear(lv_d1, lv_e1), 0, 0.35),
                      FlashAround(self.digits, color=GOLD, time_width=1.5),
                      *during(appear(tab, shift=None), 0.3, 1), run_time=1.6)  # early: ch2's table, shown whole
            self.play(GrowFromCenter(rowbox), run_time=0.9)
            c.wait_until("five used states")
            used = T("a used state", 34, GREEN).next_to(VGroup(self.lab, self.digits), DOWN, buff=0.3)
            self.used = used
            self.play(self.digits.animate.set_color(GREEN), *appear(used),
                      FlashAround(rowbox, color=GREEN, time_width=1.5), run_time=1.2)

    # -- c3.restart.2: clock back on; the ones step round; output b is the divide-by-five wave ----
    def clip2(self):
        rl, src, sh = self.rl, self.src, self.sh
        pn = S1.wave_panel().shift(PANEL_DY * DOWN)
        ghost = S1.ghost_wave((0, 0, 1, 1, 0)).shift(PANEL_DY * DOWN).set_stroke(opacity=0.25)
        self.pn, self.ghost = pn, ghost
        with self.say("c3.restart.2") as c:
            # the switch closes; CLK reaches all five flip-flops
            bright = [flip(self.sw, 1)]
            for m in S6.clk_after(sh):
                bright.append(m.animate.set_fill(opacity=1) if isinstance(m, Dot) else m.animate.set_stroke(opacity=1))
            flashes = [VShowPassingFlash(m, time_width=0.6) for m in rl.clk_paths()]
            self.play(*during(bright, 0, 0.5), *during(flashes, 0.4, 1.0),
                      run_time=min(1.4, c.until("run", floor=0.8)))
            settle(self, rl)

            # room for the waveform: the readout and table go, the ring goes back up
            c.wait_until("run")
            up = UP_DY * UP
            moving = [rl, src, self.lead, self.sw, self.link, *self.pins_s, *self.btns, *self.tokens.values()]
            self.play(  # early: the waveform panel's axes, drawn from the next beat on
                *during(disappear(self.lab, self.digits, self.used, self.tab, self.rowbox), 0, 0.4),
                *during([m.animate.shift(up) for m in moving], 0.25, 0.75),
                *during(appear(*pn.labels, ghost, shift=None, lag=0.15), 0.6, 1),
                run_time=1.2)

            src.t = 0.0

            def tick(m, dt):
                m.t += dt
                m.circle.set_fill(YELLOW, 0.6 if (m.t % self.per) < self.per / 2 else 0.0)
            self.per = per = max(0.6, c.until("thats exactly") / 10)
            src.add_updater(tick)

            bits = [0, 0, 0, 1, 1]            # a b c d e
            lo, hi = S1.W_OUT_Y - PANEL_DY - S1.W_H / 2, S1.W_OUT_Y - PANEL_DY + S1.W_H / 2
            x = pn.x
            outs, prev = [], None
            for j in range(10):
                anims = []
                if j > 0:
                    bits = [bits[(i - 1) % 5] for i in range(5)]
                    step, new = [], {}
                    for pos, m in self.tokens.items():
                        if pos < 4:
                            step.append(m.animate.move_to(self.tok_pos(pos + 1)))
                            new[pos + 1] = m
                        else:
                            step.append(FadeOut(m, shift=0.5 * RIGHT))
                            nm = self.new_tok(0)
                            step.append(FadeIn(nm, shift=0.5 * RIGHT))
                            new[0] = nm
                    self.tokens = new
                    anims += during(step, 0, 0.45) + during(self.leds_to(bits), 0.25, 0.45)
                lev = hi if bits[1] else lo
                pts = []
                if prev is not None and prev != lev:
                    pts.append(_p(x(j), prev))
                pts += [_p(x(j), lev), _p(x(j + 1), lev)]
                op = VMobject().set_points_as_corners(pts).set_stroke(GREEN, 4)
                outs.append(op)
                prev = lev
                cp = pn.clk_pieces[j]
                anims += [Create(cp.wave, rate_func=linear), FadeIn(cp.up, scale=0.5),
                          Create(op, rate_func=linear),
                          *[time_span(VShowPassingFlash(m, time_width=0.6), 0, min(0.8, per))
                            for m in rl.clk_paths()]]
                self.play(*anims, run_time=per)
                settle(self, rl)
            self.outs = outs

            # exactly the divide-by-five wave
            c.wait_until("thats exactly")
            full = VMobject()
            full.set_points_as_corners([p for o in outs for p in o.get_anchors()])
            full.set_stroke(GREEN, 10)
            self.play(VShowPassingFlash(full, time_width=0.5), FlashAround(ghost, color=GREEN, time_width=1.5),
                      run_time=2.0)
            src.clear_updaters()
            src.circle.set_fill(YELLOW, 0)

            # two lessons
            c.wait_until("lessons")
            drawn = [*pn.labels, *[p for cp in pn.clk_pieces for p in (cp.wave, cp.up)], *outs, ghost]
            self.play(*disappear(*drawn), run_time=1.0)
            l1 = T("1 · This is what asynchronous set and reset are for.", 34,
                   t2c={"asynchronous set and reset": RED})
            l2 = T("2 · A machine must start in a used state.", 34, t2c={"used state": GREEN})
            l1.move_to(_p(0, -1.45))
            l2.move_to(_p(0, -2.25)).align_to(l1, LEFT)
            self.l1, self.l2 = l1, l2
            c.wait_until("first")
            self.play(*appear(l1), run_time=1.0)
            c.wait_until("second")
            self.play(*appear(l2), run_time=1.0)
            c.wait_until("otherwise")
            # s1's scope, small: the clock runs, the output stays at 0
            sx0, sp, sh_ = 1.7, 0.95, 0.3
            cy, oy = -2.95, -3.38
            sclk = [S1.clk_period(sx0 + j * sp, cy, p=sp, h=sh_, width=3) for j in range(4)]
            flat = Line(_p(sx0, oy - sh_ / 2), _p(sx0 + 4 * sp, oy - sh_ / 2)).set_stroke(GREEN, 4)
            sclk_l = T("CLK", 28, YELLOW).next_to(_p(sx0 - 0.4, cy), LEFT, buff=0)
            out_l = T("output", 28, GREEN).next_to(_p(sx0 - 0.4, oy), LEFT, buff=0)
            zero = value_label("0", 34, GOLD).next_to(flat, RIGHT, buff=0.25).set_y(oy)
            self.flat = VGroup(*sclk, flat, sclk_l, out_l, zero)
            self.play(*appear(sclk_l, out_l, shift=None, lag=0.1),  # early: the scope's labels
                      *[FadeIn(m) for m in sclk], Create(flat, rate_func=linear), run_time=1.0)
            self.play(VShowPassingFlash(flat.copy().set_stroke(GREEN, 10), time_width=0.6),
                      *appear(zero, shift=None), FlashAround(flat, color=RED, time_width=1.5),
                      run_time=min(1.4, c.until(floor=0.8)))
            settle(self, self.flat)

    # -- c3.restart.3: the start-up pulse ------------------------------------------------------------
    def clip3(self):
        rl, ffs = self.rl, self.ffs
        with self.say("c3.restart.3") as c:
            # nobody presses buttons: they go, and the power is off
            self.play(*disappear(*self.btns, *self.tokens.values()),
                      *self.leds_to([0] * 5), *set_alpha([self.rc.out_l], 0), run_time=1.2)
            settle(self, rl)

            # the network: R pins on a, b, c; one RED line from a power switch
            rpins = []
            for f in ffs[:3]:
                s = f.box.width / BOX_W
                L = (f.box.get_bottom()[1] - 2 * BUB_R * s - BUS_Y) / s
                p = S6.pin(f, "R", size=28, length=L)
                p.label.next_to(p.wire.get_end(), DR, buff=0.06)
                rpins.append(p)
            y_top = self.pins_s[0].wire.get_end()[1]
            power = S6.toggle(0, RED).move_to(_p(RISER_X, -1.45)).set_z_index(2)
            pw_lab = T("power", 30, RED).next_to(power, DOWN, buff=0.2)
            x0 = rpins[0].wire.get_end()[0]
            bottom = Line(_p(x0, BUS_Y), _p(RISER_X, BUS_Y))
            riser = Line(power.get_top(), _p(RISER_X, y_top))
            top = Line(_p(RISER_X, y_top), _p(self.pins_s[0].wire.get_end()[0], y_top))
            net = [bottom, riser, top]
            for ln in net:
                ln.set_stroke(RED, 4)
            dots = [Dot(_p(RISER_X, BUS_Y), radius=0.07, color=RED)] + \
                   [Dot(_p(p.wire.get_end()[0], BUS_Y), radius=0.07, color=RED) for p in rpins[1:]] + \
                   [Dot(_p(self.pins_s[1].wire.get_end()[0], y_top), radius=0.07, color=RED)]
            self.power = power
            self.play(*during(disappear(self.l1, self.l2, self.flat), 0, 0.35),  # early: the circuit's power switch
                      *during([GrowFromCenter(p.bub) for p in rpins], 0, 0.4),
                      *during([GrowFromEdge(p.wire, UP) for p in rpins], 0.2, 0.7),
                      *during([Create(ln) for ln in net], 0.3, 1),
                      *during([FadeIn(d) for d in dots], 0.7, 1),
                      *during(appear(power, pw_lab, *[p.label for p in rpins], shift=None, lag=0.1), 0.4, 1),
                      run_time=min(1.5, 0.6 * c.until("pulse")))
            # power on: the flip-flops wake up in some pattern
            self.play(flip(power, 1), *self.leds_to([1, 0, 1, 0, 0]), run_time=min(0.8, c.until("pulse", floor=0.5)))
            settle(self, rl)

            wires = [p.wire for p in rpins] + [p.wire for p in self.pins_s]

            def pulse():
                return [VShowPassingFlash(m.copy().set_stroke(RED, 10), time_width=0.7) for m in net + wires]
            c.wait_until("pulse")
            self.play(*pulse(), *during(self.leds_to([0, 0, 0, 1, 1]), 0.5, 1), run_time=1.4)
            settle(self, rl)

            cap = VGroup(T("“Often used to force a synchronous circuit", 32),
                         T("into a known state, say at start-up.”", 32)).arrange(DOWN, buff=0.22)
            cap.move_to(_p(-0.6, -2.35))
            src_l = T("p. 91", 28, DIM).next_to(cap, RIGHT, buff=0.35).align_to(cap, DOWN)
            c.wait_until(own_word=cap[0])
            self.play(*appear(*cap, src_l, lag=0.3), run_time=1.4)
            c.wait_until("sets the last two")
            self.play(*pin_pulse(self.pins_s), run_time=1.2)
            c.wait_until("resets the rest")
            self.play(*pin_pulse(rpins), run_time=1.2)

            # every power-up lands on 11000
            c.wait_until("every")
            cyc = max(0.9, c.until(floor=0.9) / 3)
            for pat in ([0, 1, 1, 0, 1], [1, 1, 0, 0, 1], [0, 1, 0, 1, 0]):
                self.play(flip(power, 0), *self.leds_to([0] * 5), run_time=0.25 * cyc)
                self.play(flip(power, 1), *self.leds_to(pat), run_time=0.3 * cyc)
                self.play(*pulse(), *during(self.leds_to([0, 0, 0, 1, 1]), 0.4, 1), run_time=0.45 * cyc)
                settle(self, rl)
