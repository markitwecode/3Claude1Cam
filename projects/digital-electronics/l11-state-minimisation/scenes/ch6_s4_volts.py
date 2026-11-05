"""Chapter 6, scene 4: volts, energy per coulomb (emf V_B, pd V_L). Clips c6.volts.1 – c6.volts.4.

Builds on s2's running loop (circuit drawings from ch6_s2_electrons). A lamp drops into the slot,
a GOLD "1 C" token rides clockwise with the current, picks up energy in the battery and gives it
up in the lamp; emf and pd are named, V_L = E/Q, both are voltages, arrows point to the higher end.
Ends on handover_shot() (s5's first frame).
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

S2 = load_scene("ch6_s2_electrons")
HEAT = S2.HEAT

# geometry of s2's Loop(): x ±3.8, y −2.7 … 1.9, battery and slot at y −0.4
CUR = ((-1.0, 1.9, 0), (1.0, 1.9, 0))            # GOLD current arrow on the top wire (left → right)
VB_LOW, VB_HIGH = (-4.5, -0.9, 0), (-4.5, 0.1, 0)  # TEAL V_B, left of the battery, head at "+"
VL_LOW, VL_HIGH = (4.6, -1.05, 0), (4.6, 0.25, 0)  # TEAL V_L, right of the lamp, head at its top


def _loop_with_slot_open():
    loop = S2.Loop()
    loop.wire.remove(loop.slot_fill)
    return loop


def handover_shot():
    """This scene's last frame, s5's first: the loop with the lit lamp in its slot, the GOLD current
    arrow on the top wire (clockwise, no label), TEAL V_B (left of the battery) and V_L (right of the
    lamp) labelled. VGroup(loop, lamp, cur, vb, vl), also as .loop .lamp .cur .vb .vl."""
    loop = _loop_with_slot_open()
    lmp = loop.place(S2.lamp(lit=True))
    lmp.shift(loop.slot_center() - lmp.circle.get_center())
    cur = S2.current_arrow(*CUR)
    vb = S2.voltage_arrow(VB_LOW, VB_HIGH, "V_B", side=LEFT)
    vl = S2.voltage_arrow(VL_LOW, VL_HIGH, "V_L", side=RIGHT)
    g = VGroup(loop, lmp, cur, vb, vl)
    g.loop, g.lamp, g.cur, g.vb, g.vl = loop, lmp, cur, vb, vl
    return g


# --- the token's clockwise ride -------------------------------------------------------------
_CORNERS = [np.array(p, dtype=float) for p in ((-3.8, -2.7, 0), (-3.8, 1.9, 0), (3.8, 1.9, 0), (3.8, -2.7, 0))]
_NORMALS = [LEFT, UP, RIGHT, DOWN]          # outward normal of each side (left, top, right, bottom)
_LENS = [4.6, 7.6, 4.6, 7.6]


def ride_point(s):
    """Point at distance s clockwise round the loop from the bottom-left corner, and a smoothed
    outward normal (blended over 0.6 either side of each corner)."""
    P = sum(_LENS)
    s = s % P
    k = 0
    while s > _LENS[k]:
        s -= _LENS[k]
        k += 1
    a, b = _CORNERS[k], _CORNERS[(k + 1) % 4]
    p = a + (b - a) * (s / _LENS[k])
    d = 0.6
    n = _NORMALS[k].astype(float)
    if s > _LENS[k] - d:
        w = 0.5 * (s - (_LENS[k] - d)) / d
        n = (1 - w) * n + w * _NORMALS[(k + 1) % 4]
    elif s < d:
        w = 0.5 * (d - s) / d
        n = (1 - w) * n + w * _NORMALS[(k - 1) % 4]
    return p, n / np.linalg.norm(n)


def chip_offset(chip, n, r):
    ext = abs(n[0]) * chip.width / 2 + abs(n[1]) * chip.height / 2
    return n * (r + 0.14 + ext)


TOK_R = 0.38


def token():
    ring = Circle(radius=TOK_R).set_stroke(GOLD, 4).set_fill(BG, 1)
    lab = T("1 C", 28, GOLD).move_to(ring)
    g = VGroup(ring, lab).set_z_index(3)
    return g


def chip(txt):
    lab = T(txt, 30, GOLD)
    box = RoundedRectangle(corner_radius=0.12, width=lab.width + 0.36, height=0.52)
    box.set_stroke(GOLD, 2.5).set_fill(BG, 1)
    return VGroup(box, lab.move_to(box)).set_z_index(3)


def cell_15():
    """A small AA cell lying on its side, '+' nub on the right, '1.5 V' printed on it."""
    body = RoundedRectangle(corner_radius=0.08, width=1.45, height=0.56).set_stroke(FG, 3).set_fill(BG, 1)
    nub = Rectangle(width=0.1, height=0.22).set_stroke(FG, 3).set_fill(FG, 1).next_to(body, RIGHT, buff=0)
    lab = T("1.5 V", 28, GOLD).move_to(body)
    g = VGroup(body, nub, lab)
    g.lab = lab
    return g


class Volts(NarratedScene):
    def construct(self):
        loop = _loop_with_slot_open()
        fill = S2.Loop().slot_fill          # drawn where the lamp will go, until it drops in
        self.play(FadeIn(loop), FadeIn(fill), run_time=1.0)
        self.wait(0.3)
        self.loop, self.fill = loop, fill
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()

    # ------------------------------------------------------------------------------------------
    def clip1(self):
        loop, bat = self.loop, self.loop.battery
        lmp = S2.lamp(lit=False)
        lmp.shift(loop.slot_center() - lmp.circle.get_center())
        lamp_lab = T("Lamp", 32).next_to(lmp.circle, UR, buff=0.12).shift(RIGHT * 0.2)
        cur = S2.current_arrow(*CUR, label="Flow of current", side=UP)
        cell = cell_15().move_to([-1.75, -0.4, 0])
        emf_cap = T("electromotive force (emf)", 30).next_to(cell, DOWN, buff=0.38).align_to(cell, LEFT)
        vb = S2.voltage_arrow(VB_LOW, VB_HIGH, "V_B", side=LEFT)
        path = VMobject().set_points_as_corners([[-3.8, 0.0, 0], [-3.8, 1.9, 0], [3.8, 1.9, 0],
                                                 [3.8, -2.7, 0], [-3.8, -2.7, 0], [-3.8, -0.8, 0]])
        path.set_stroke(YELLOW, 7)

        with self.say("c6.volts.1") as c:
            self.play(FadeOut(self.fill), FadeIn(lmp, shift=0.5 * DOWN), run_time=1.0)
            self.play(*appear(lamp_lab), GrowArrow(cur.arrow), run_time=0.9)
            self.play(*appear(cur.label), run_time=0.8)  # early: p. 167's label on the drawn arrow
            c.wait_until("force")
            self.play(bat.animate(rate_func=there_and_back).scale(1.18),
                      VShowPassingFlash(path, time_width=0.35), run_time=2.0)
            c.wait_until("printed")
            self.play(FadeIn(cell, shift=0.25 * RIGHT), run_time=1.0)
            c.wait_until("one and a half")
            self.play(FlashAround(cell.lab, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("emf")
            self.play(*appear(emf_cap), GrowArrow(vb.arrow), run_time=1.2)
            c.wait_until("vee")
            self.play(*appear(vb.label), run_time=0.9)
        self.lmp, self.lamp_lab, self.cur, self.cell, self.emf_cap, self.vb = lmp, lamp_lab, cur, cell, emf_cap, vb

    # ------------------------------------------------------------------------------------------
    def clip2(self):
        card = VGroup(
            Tex(r"emf ", r"$V_B$", r" = 1\,V if it gives ", r"1\,J", font_size=38),
            Tex(r"of electrical energy to each ", r"C", font_size=38),
            Tex(r"of charge passing through it", font_size=38),
        ).arrange(DOWN, buff=0.12).move_to([0.1, 0.8, 0])
        card[0][1].set_color(TEAL)
        card[0][3].set_color(GOLD)
        tok = token()
        p0, _ = ride_point(0.9)
        tok.move_to(p0)
        s = ValueTracker(0.9)
        tok.add_updater(lambda m: m.move_to(ride_point(s.get_value())[0]))
        park = 3.3
        chip1 = chip("+1 J")
        pp, nn = ride_point(park)
        chip1.move_to(pp + chip_offset(chip1, nn, TOK_R))
        chip2 = chip("+1.5 J")
        chip2.move_to(pp + chip_offset(chip2, nn, TOK_R))

        with self.say("c6.volts.2") as c:
            self.play(*appear(*card, lag=0.3), run_time=1.6)  # early: the definition card, read out next
            c.wait_until("joule")
            self.play(FadeIn(tok, scale=0.6), run_time=0.8)
            self.play(s.animate.set_value(park), run_time=2.4, rate_func=smooth)
            self.play(FadeIn(chip1, shift=0.2 * LEFT), FlashAround(self.loop.battery, run_time=1.2),
                      run_time=1.2)
            c.wait_until("half")
            self.play(*swap(chip1, chip2), FlashAround(self.cell.lab, run_time=1.4, time_width=1.5),
                      run_time=1.4)
        tok.clear_updaters()
        self.card, self.tok, self.chip, self.s = card, tok, chip2, s

    # ------------------------------------------------------------------------------------------
    def clip3(self):
        loop, lmp, cur, tok, ch, s = self.loop, self.lmp, self.cur, self.tok, self.chip, self.s
        lamp_s = 4.6 + 7.6 + 2.3
        tok.add_updater(lambda m: m.move_to(ride_point(s.get_value())[0]))

        def chip_upd(m):
            p, n = ride_point(s.get_value())
            m.move_to(p + chip_offset(m, n, TOK_R))
        ch.add_updater(chip_upd)
        ctr = lmp.circle.get_center()
        rays = VGroup(*[Line(ctr + 0.62 * np.array([np.cos(a), np.sin(a), 0]),
                             ctr + 1.12 * np.array([np.cos(a), np.sin(a), 0]))
                        for a in np.arange(10) * TAU / 10 + TAU / 20]).set_stroke(YELLOW, 4)
        rings = VGroup(*[Circle(radius=0.5).move_to(ctr).set_stroke(HEAT, 6, opacity=0.8) for _ in range(2)])
        glow = S2.lamp_glow(lmp)
        vl = S2.voltage_arrow(VL_LOW, VL_HIGH, "V_L", side=RIGHT)
        pd_cap = T("potential difference (pd)", 30).move_to([0, -2.2, 0]).align_to([3.3, 0, 0], RIGHT)
        ratio = MathTex(r"V_L", r"=", r"\frac{E}{Q}", font_size=56).move_to([-1.3, 0.92, 0])
        ratio[0].set_color(TEAL)
        E, Q = ratio[2][0], ratio[2][2]
        e_tag = T("energy (J)", 30, GOLD).next_to(ratio, RIGHT, buff=0.45).set_y(E.get_y())
        q_tag = T("charge (C)", 30).next_to(ratio, RIGHT, buff=0.45).set_y(Q.get_y())
        unit = MathTex(r"1\,\text{V} = 1\,\text{J}/\text{C}", font_size=48).move_to([0.6, -0.5, 0])

        with self.say("c6.volts.3") as c:
            ride_t = max(1.8, c.until("heat") + 0.4)
            self.play(*during(disappear(self.card, self.cell, self.lamp_lab, cur.label), 0, 0.3),
                      *during([UpdateFromAlphaFunc(tok, lambda m, a, s0=s.get_value(): s.set_value(s0 + (lamp_s - s0) * smooth(a)))], 0.15, 1.0),
                      run_time=ride_t)
            cur.remove(cur.label)
            ch.clear_updaters()
            tok.clear_updaters()
            self.play(*during([FadeOut(ch, scale=0.6)], 0, 0.35),
                      *during([Create(r) for r in rays], 0.2, 0.7),
                      *during([r.animate.scale(2.6).set_stroke(opacity=0) for r in rings], 0.25, 1.0),
                      *during([FadeIn(glow)], 0.3, 1.0), run_time=1.6)
            lmp.glow = glow
            lmp.add_to_back(glow)
            self.remove(*rings)
            self.play(FadeOut(rays), FadeOut(tok, shift=0.8 * DOWN), run_time=1.0)
            c.wait_until("pd")
            self.play(GrowArrow(vl.arrow), *appear(pd_cap), run_time=1.2)
            c.wait_until("vee")
            self.play(*appear(vl.label), run_time=0.9)
            c.wait_until("converts")
            self.play(FlashAround(lmp.circle, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("ratio")
            self.play(*appear(ratio), run_time=1.0)
            c.wait_until(own_word=e_tag)
            self.play(*appear(e_tag), run_time=0.8)
            c.wait_until(own_word=q_tag)
            self.play(*appear(q_tag), run_time=0.8)
            c.wait_until("joules per coulomb")
            self.play(*appear(unit), run_time=0.9)
        self.vl, self.pd_cap, self.ratio, self.e_tag, self.q_tag, self.unit = vl, pd_cap, ratio, e_tag, q_tag, unit

    # ------------------------------------------------------------------------------------------
    def clip4(self):
        loop, vb, vl, cur = self.loop, self.vb, self.vl, self.cur
        gives = T("emf: energy given\nto each coulomb", 30, t2c={"emf:": TEAL}).move_to([0, -1.45, 0])
        gives.align_to([-3.2, 0, 0], LEFT)
        takes = T("pd: energy taken\nfrom each coulomb", 30, t2c={"pd:": TEAL}).move_to([0, 0.95, 0])
        takes.align_to([2.8, 0, 0], RIGHT)
        both = T("both measured in V", 32).move_to(self.unit)
        volts = T("voltages", 50, TEAL).move_to([0, 0.5, 0])
        head = T("head at the higher potential", 32, TEAL).move_to([0, -1.35, 0])
        right_wire = Line([3.8, 1.9, 0], [3.8, 0.25, 0]).set_stroke(GOLD, 8)

        with self.say("c6.volts.4") as c:
            self.play(*swap(self.emf_cap, gives), run_time=1.3)
            c.wait_until("takes")
            self.play(*during(disappear(self.ratio, self.e_tag, self.q_tag, self.pd_cap), 0, 0.45),
                      *during(appear(takes), 0.5, 1.0), run_time=1.5)
            c.wait_until("volts")
            self.play(*swap(self.unit, both), run_time=1.2)
            c.wait_until(own_word=volts)
            self.play(*during([gives.animate.scale(0.7).set_opacity(0),
                               takes.animate.scale(0.7).set_opacity(0)], 0, 0.5),
                      *during(appear(volts, shift=None), 0.5, 1.0), run_time=1.6)
            self.remove(gives, takes)
            c.wait_until("arrows")
            self.play(*flash([vb.arrow, vl.arrow], color=TEAL, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until(own_word=head)
            self.play(*appear(head), run_time=1.0)
            c.wait_until("ends")
            self.play(*flash([vb.arrow.tip, loop.battery.plus_sign], run_time=1.2, time_width=1.0),
                      run_time=1.2)
            c.wait_until("for the lamp")
            self.play(VShowPassingFlash(right_wire, time_width=0.5),
                      *flash([vl.arrow.tip], run_time=1.6, time_width=1.5), run_time=1.6)
        self.play(*disappear(volts, both, head), run_time=1.0)
        # swap in the exact handover picture (same geometry, drawn identically)
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(1.0)
