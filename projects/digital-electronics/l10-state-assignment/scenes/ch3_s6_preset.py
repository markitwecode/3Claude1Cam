"""Chapter 3, scene 6: asynchronous set, active low. Clips c3.preset.1 – c3.preset.3.

The ring is ch3_s1_hook's ring_leds(), lowered by RING_DY, with a ticking YELLOW clock source and a
switch (L6's toggle) on the CLK line, and a "state 00000" readout. Flip-flop c comes forward,
enlarged, as the 74HC74; RED S / R pins (L6 ch3_s6's pin(), with the active-low bubble) grow out.

Shared (s7 opens on handover_shot() and reuses these; all standalone):
  preset_ring(open_=True)   ring + clock source + switch + readout; .rl .rc .src .lead .sw .link
                            .readout .digits; open_: switch off and the CLK line after it dark.
  clk_after(g)              the CLK pieces after the switch (bus, link, dots, every clock pin).
  toggle(v, color) / flip(sw, v)    L6's slide switch (knob right + coloured = closed).
  pin(ff, kind, size, length)       RED "S" (top) / "R" (bottom, CLR_DX right of the clock pin)
                            with bubble; VGroup(bub, wire, label), .bub .wire .label .end.
  push_button(s) / place_button(btn, p) / press(btn, down)   housing + YELLOW cap; press sinks it.
  handover_shot()           preset_ring(open) + S pins and push buttons on d and e (.extras).
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

S1 = load_scene("ch3_s1_hook")
set_led = S1.set_led
BOX_W = S1.BOX_W
EN_WIRE = 1.0
CLR_DX = 0.55
S_DX = 0.45                       # native: S pin left of the box centre (the LED sits right of it)
S_LAB_MAX = 1.0
BUB_R = 0.1
RING_DY = 0.6
CLK_DARK = 0.22


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- switch (L6 ch3_s6_async's toggle) ------------------------------------------------------------
def toggle(v, color=BLUE):
    g = VGroup()
    track = RoundedRectangle(corner_radius=0.19, width=0.78, height=0.38).set_stroke(color, 3).set_fill(BG, 1)
    knob = Circle(radius=0.13).set_stroke(width=0)
    g.add(track, knob)
    g.track, g.knob, g.v, g.sw_color = track, knob, v, color

    def knob_pos(val):
        return g.track.get_center() + (0.2 if val else -0.2) * g.track.width / 0.78 * RIGHT
    g.knob_pos = knob_pos
    knob.move_to(knob_pos(v)).set_fill(color if v else DIM, 1)
    return g


def flip(sw, v):
    sw.v = v
    return sw.knob.animate.move_to(sw.knob_pos(v)).set_fill(sw.sw_color if v else DIM, 1)


# ---- async pins (L6 ch3_s6_async's pin(), S / R with the active-low bubble) -----------------------
def pin(ff, kind, size=30, length=None):
    """A RED async pin out of the box: S on top (S_DX left of centre, clear of the LED over the Q
    side, label on the wire's left), R underneath (CLR_DX right of the clock pin, label right).
    A small bubble sits on the box edge, the wire runs outwards from it. `length` (native units)
    is the wire beyond the bubble."""
    s = ff.box.width / BOX_W
    c, hb = ff.box.get_center(), ff.box.height / 2
    r = BUB_R * s
    L = (length if length is not None else EN_WIRE) * s
    d = UP if kind == "S" else DOWN
    a = c - S_DX * s * RIGHT + hb * UP if kind == "S" else c + CLR_DX * s * RIGHT + hb * DOWN
    bub = Circle(radius=r).set_stroke(RED, 3).set_fill(BG, 1).move_to(a + r * d)
    w = Line(a + 2 * r * d, a + (2 * r + L) * d).set_stroke(RED, 5)
    lab = T(kind, size, RED).next_to(w, LEFT if kind == "S" else RIGHT, buff=0.12)
    if kind == "S" and length is not None and length > S_LAB_MAX:
        lab.set_y(a[1] + (2 * r + 0.5 * S_LAB_MAX) * s)   # stays below the feedback wire
    g = VGroup(bub, w, lab)
    g.bub, g.wire, g.label, g.end = bub, w, lab, w.get_end()
    return g


# ---- push button: housing with a YELLOW cap that sinks when pressed -------------------------------
def push_button(s=1.0):
    house = Rectangle(width=0.6 * s, height=0.28 * s).set_stroke(FG, 3).set_fill(BG, 1).set_z_index(2)
    cap = Rectangle(width=0.34 * s, height=0.18 * s).set_stroke(width=0).set_fill(YELLOW, 1).set_z_index(1)
    cap.next_to(house, UP, buff=0)
    g = VGroup(house, cap)
    g.house, g.cap, g.s, g.down = house, cap, s, False
    return g


def place_button(btn, p):
    """Housing's bottom centre on point p (a pin's .end)."""
    return btn.shift(p - btn.house.get_bottom())


def press(btn, down=True):
    k = (1 if down else -1) if down != btn.down else 0
    btn.down = down
    return btn.cap.animate.shift(0.15 * btn.s * k * DOWN)


# ---- clock source ----------------------------------------------------------------------------------
def clock_source():
    ring = Circle(radius=0.3).set_stroke(YELLOW, 4).set_fill(YELLOW, 0)
    w, h = 0.16, 0.11
    wave = VMobject().set_points_as_corners(
        [_p(-1.5 * w, -h), _p(-w / 2, -h), _p(-w / 2, h), _p(w / 2, h), _p(w / 2, -h), _p(1.5 * w, -h)]
    ).set_stroke(YELLOW, 3)
    g = VGroup(ring, wave)
    g.circle, g.wave = ring, wave
    return g


# ---- the ring with clock source, switch and readout ------------------------------------------------
def preset_ring(open_=True):
    rl = S1.ring_leds().shift(RING_DY * DOWN)
    rc = rl.rc
    y, x0 = rc.clk.get_y(), rc.clk.get_left()[0]
    sw = toggle(0 if open_ else 1, YELLOW).scale(0.75).move_to(_p(-5.15, y)).set_z_index(2)
    src = clock_source().move_to(_p(-6.15, y))
    lead = Line(src.get_right(), sw.get_left()).set_stroke(YELLOW, 5)
    link = Line(sw.get_right(), _p(x0, y)).set_stroke(YELLOW, 5)
    rc.clk_l.next_to(src, UP, buff=0.18)
    lab = T("state", 32, DIM)
    digits = Mono("00000", 44, FG)
    readout = VGroup(lab, digits).arrange(RIGHT, buff=0.3).move_to(_p(2.6, -1.75))
    g = VGroup(rl, src, lead, sw, link, readout)
    g.rl, g.rc, g.src, g.lead, g.sw, g.link, g.readout, g.digits = rl, rc, src, lead, sw, link, readout, digits
    if open_:
        for m in clk_after(g):
            dark(m)
    return g


def clk_after(g):
    rc = g.rc
    return [rc.clk, g.link, *rc.dots, *[f.clk_w for f in rc.ffs]]


def dark(m, op=CLK_DARK):
    if isinstance(m, Dot):
        return m.set_fill(opacity=op)
    return m.set_stroke(opacity=op)


def ring_extras(g):
    """S pins and push buttons on flip-flops d and e (what s7 presses)."""
    out = []
    for f in g.rc.ffs[3:]:
        p = pin(f, "S", size=28, length=1.85)    # crosses the feedback (no dot); button above it
        b = place_button(push_button(f.box.width / BOX_W), p.end)
        out += [p, b]
    return out


def handover_shot():
    g = preset_ring(open_=True)
    ex = ring_extras(g)
    g.add(*ex)
    g.extras = ex
    return g


# ---- the enlarged flip-flop ------------------------------------------------------------------------
HERO_C = _p(-2.5, -0.25)
HERO_S = 1.3                      # box scale (native box 1.5 wide)
CAP_SIZE = 34


class Preset(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.finale()

    # -- c3.preset.1: the clock is disconnected; flip-flop c comes forward with S and R -----------
    def clip1(self):
        with self.say("c3.preset.1") as c:
            g = preset_ring(open_=False)
            self.g = g
            src = g.src
            src.t, src.closed = 0.0, True
            after = clk_after(g)

            def tick(m, dt):
                m.t += dt
                on = (m.t % 1.0) < 0.5
                m.circle.set_fill(YELLOW, 0.6 if on else 0.0)
                g.lead.set_stroke(opacity=1.0 if on else 0.45)
                if m.closed:
                    for p in after:
                        if isinstance(p, Dot):
                            p.set_fill(opacity=1.0 if on else 0.45)
                        else:
                            p.set_stroke(opacity=1.0 if on else 0.45)

            self.play(FadeIn(g), run_time=1.2)
            src.add_updater(tick)
            c.wait_until("switch")

            # the switch opens: the clock still ticks before it, the line after it goes dark
            src.closed = False
            anims = [flip(g.sw, 0)]
            for p in after:
                anims.append(p.animate.set_fill(opacity=CLK_DARK) if isinstance(p, Dot)
                             else p.animate.set_stroke(opacity=CLK_DARK))
            self.play(*anims, run_time=1.2)
            settle(self, g)
            cap = T("clock disconnected", 32, YELLOW).move_to(_p(-4.6, -1.5))
            self.cap_clk = cap
            c.wait_until(own_word=cap)
            self.play(*appear(cap), run_time=1.0)
            c.wait_until("opened a switch")
            self.play(FlashAround(g.sw, run_time=1.5, time_width=1.5))
            c.wait_until("lecture6")

            # flip-flop c comes forward, enlarged
            src.clear_updaters()
            rl, rc = g.rl, g.rc
            ffc, stub, led = rc.ffs[2], rl.stubs[2], rl.leds[2]
            self.home = ffc.box.get_center().copy()
            self.k = HERO_S / (ffc.box.width / BOX_W)
            rc.remove(ffc)
            rl.remove(stub, led)
            hero = VGroup(ffc, stub, led)
            self.add(hero)
            self.hero, self.ffc, self.led = hero, ffc, led
            hero.generate_target()
            hero.target.scale(self.k, about_point=self.home).shift(HERO_C - self.home)
            self.play(*during(disappear(g, cap), 0, 0.4), *during(MoveToTarget(hero), 0.4, 1.0),
                      run_time=min(2.4, c.until("lecture six")))
            chip = T("74HC74", 34, DIM).move_to(_p(-4.7, -1.15))
            self.chip = chip
            self.play(*appear(chip), run_time=1.0)  # early: the chip's part number, "a real chip" in the next line
            c.wait_until("pins")

            # S and R grow out of the box
            ps = pin(ffc, "S", size=44, length=0.75)
            pr = pin(ffc, "R", size=44, length=0.5)
            self.ps, self.pr = ps, pr
            self.play(GrowFromCenter(ps.bub), GrowFromCenter(pr.bub), run_time=0.6)
            self.play(GrowFromEdge(ps.wire, DOWN), GrowFromEdge(pr.wire, UP), run_time=1.2)
            cap_s = T("Preset/Set – force Q to 1", CAP_SIZE, FG, t2c={"Preset/Set": RED})
            cap_s.move_to(_p(-1.6, 2.92), aligned_edge=LEFT)
            cap_r = T("Reset/Clear – force Q to 0", CAP_SIZE, FG, t2c={"Reset/Clear": RED})
            cap_r.move_to(_p(-1.0, pr.wire.get_center()[1]), aligned_edge=LEFT)
            self.cap_s, self.cap_r = cap_s, cap_r
            c.wait_until("set input")
            self.play(*appear(ps.label, cap_s, lag=0.3), run_time=1.0)
            c.wait_until("reset input")
            self.play(*appear(pr.label, cap_r, lag=0.3), run_time=1.0)
            c.wait_until("now")

            now = VGroup(T("take effect independently", 32, FG),
                         T("of any clock or enable inputs", 32, FG)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            now.move_to(_p(0.6, 0.45), aligned_edge=LEFT)
            self.now = now
            self.play(*appear(*now, lag=0.4), run_time=1.4)  # early: the p. 91 line, said as "act at once"
            c.wait_until("set forces")
            self.play(FlashUnder(select(cap_s, "force Q to 1")[0], run_time=1.5, time_width=1.5))
            c.wait_until("reset forces")
            self.play(FlashUnder(select(cap_r, "force Q to 0")[0], run_time=1.5, time_width=1.5))

    # -- c3.preset.2: the bubble means active low; normally S sits at 1 -----------------------------
    def clip2(self):
        with self.say("c3.preset.2") as c:
            ps = self.ps
            self.play(*set_alpha([self.now], 0.4),
                      FlashAround(VGroup(ps.wire, ps.label), run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("little circle")
            ring = Circle(radius=0.32).set_stroke(YELLOW, 5).move_to(ps.bub.get_center())
            near = [self.led, self.hero[1]]          # the LED and its stub sit beside the S pin: dim them
            self.play(GrowFromCenter(ring), *set_alpha(near, DIMMED), run_time=1.0)
            c.wait_until("low")
            low = T("active low: 0 = do it", 32, FG, t2c={"active low": YELLOW})
            low.move_to(_p(-1.1, 2.25), aligned_edge=LEFT)
            self.low = low
            c.wait_until(own_word=low)
            self.play(*appear(low), run_time=1.0)
            c.wait_until("idle")

            lvl = value_label("1", 44, GOLD).next_to(ps.label, LEFT, buff=0.25)
            self.lvl = lvl
            self.play(*disappear(ring), *set_alpha(near, 1), *during(appear(lvl), 0.3, 1.0), run_time=1.2)
            btn = place_button(push_button(1.3), ps.end)
            self.btn = btn
            c.wait_until("push button")
            self.play(FadeIn(btn, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("press it")
            self.play(FlashAround(btn, time_width=1.5), run_time=min(1.2, c.until()))

    # -- c3.preset.3: press, Q jumps; release, Q stays; held at 0, D and the clock are ignored ------
    def clip3(self):
        with self.say("c3.preset.3") as c:
            btn, ffc = self.btn, self.ffc
            lvl0 = value_label("0", 44, RED).move_to(self.lvl)
            self.play(press(btn), *swap(self.lvl, lvl0), run_time=1.2)
            settle(self, btn)
            self.lvl = lvl0
            c.wait_until("jump")
            self.play(set_led(self.led, True), FlashAround(self.led, run_time=1.4, time_width=1.5),
                      run_time=1.4)
            settle(self, self.hero)
            c.wait_until("release")
            lvl1 = value_label("1", 44, GOLD).move_to(self.lvl)
            self.play(press(btn, False), *swap(self.lvl, lvl1), run_time=1.2)
            settle(self, btn)
            self.lvl = lvl1
            c.wait_until("stays at one")
            self.play(FlashAround(self.led, run_time=1.2, time_width=1.5))
            c.wait_until("held")

            # replay: S held at 0 while D = 0 and a clock edge arrive
            lvl0 = value_label("0", 44, RED).move_to(self.lvl)
            self.play(press(btn), *swap(self.lvl, lvl0), run_time=1.2)
            settle(self, btn)
            self.lvl = lvl0
            held = VGroup(T("held at 0: ignores D", 32, FG),
                          T("and the clock", 32, FG)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            held.move_to(self.now, aligned_edge=LEFT)
            c.wait_until(own_word=held[0])
            self.play(*disappear(self.now), run_time=0.6)
            self.play(*appear(*held, lag=0.3), run_time=1.0)
            self.now = held
            c.wait_until("whatever arrives")
            d0 = value_label("0", 44, GOLD).next_to(ffc.d_w, LEFT, buff=0.15)
            self.d0 = d0
            self.play(*appear(d0), run_time=0.9)
            edge = ffc.clk_w.copy().set_stroke(YELLOW, 10, opacity=1)
            self.play(VShowPassingFlash(edge, time_width=0.6), run_time=1.2)
            self.play(FlashAround(self.led, run_time=1.2, time_width=1.5))
            c.wait_until("normal")

            lvl1 = value_label("1", 44, GOLD).move_to(self.lvl)
            normal = T("normal D flip-flop", 32, GREEN).move_to(self.now, aligned_edge=LEFT)
            self.play(press(btn, False), *swap(self.lvl, lvl1), *swap(self.now, normal),
                      run_time=min(1.2, c.until()))
            settle(self, btn)
            self.lvl, self.now = lvl1, normal

    # -- silent tail: c goes back into the ring; S pins and buttons appear on d and e -------------
    def finale(self):
        g, hero = self.g, self.hero
        self.wait(1.4)
        rest = [self.chip, self.ps, self.pr, self.cap_s, self.cap_r, self.now, self.low, self.lvl,
                self.btn, self.d0]
        hero.generate_target()
        hero.target.shift(self.home - HERO_C).scale(1 / self.k, about_point=self.home)
        hero.target[2].set_stroke(DIM, 3).set_fill(BG, 0)
        g.sw.set_z_index(2)
        g.src.circle.set_fill(YELLOW, 0)
        g.lead.set_stroke(opacity=1)
        self.play(*during(disappear(*rest), 0, 0.3), *during(MoveToTarget(hero), 0.3, 0.8),
                  *during(FadeIn(g), 0.62, 1.0), run_time=2.4)
        final = handover_shot()
        ex = final.extras
        final.remove(*ex)
        self.remove(*self.mobjects)
        self.add(final)
        self.play(*appear(*ex, lag=0.3), run_time=1.4)
        final.add(*ex)
        settle(self, final)
        self.wait(1.0)
