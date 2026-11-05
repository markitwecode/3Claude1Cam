"""Chapter 6, scene 2: electrons in a metal, and the running battery loop. Clips c6.metal.1 – c6.metal.4.

Owns the chapter's circuit drawings (kept for Lecture 12). Other scenes import them with
load_scene("ch6_s2_electrons"):
  electron(r) · ion(r) · lattice(cols, rows, pitch, r) · battery() · lamp(lit) · lamp_glow(lamp)
  resistor(label, vertical) · current_arrow(start, end, label, side) · voltage_arrow(low, high, label, side)
  Loop() (the running loop: battery left, slot in the right-hand wire) · LoopElectrons(loop)
  opening_shot() (s1's last frame, this scene's first) · handover_shot() (this scene's last, s3's first)
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
from lib.style import *  # noqa: E402,F403

# ---------------------------------------------------------------------------------------------
# Circuit drawings (chapter 6 colours: electrons BLUE "−", ions DIM "+", current GOLD, voltage TEAL,
# symbols FG, lit lamp YELLOW glow)
# ---------------------------------------------------------------------------------------------
WIRE_W = 4                 # wire stroke
LOOP_W, LOOP_H = 7.6, 4.6  # the running loop's rectangle
LOOP_C = np.array([0.0, -0.4, 0.0])
BAT_H = 0.8                # gap the battery (with its leads) fills in the left-hand wire
SLOT_H = 1.3               # gap a lamp or resistor (with leads) fills in the right-hand wire
LOOP_N = 28                # electrons round the loop
HEAT = "#FF862F"           # decorative warmth (no colour role)


def electron(r=0.14):
    """BLUE dot with a "−" (drawn, not a glyph)."""
    disk = Circle(radius=r).set_fill(BLUE, 1).set_stroke(width=0)
    bar = Line(LEFT * 0.55 * r, RIGHT * 0.55 * r).set_stroke(BG, max(2, 22 * r))
    return VGroup(disk, bar)


def ion(r=0.3):
    """DIM circle with a "+" (drawn): a fixed positive ion."""
    ring = Circle(radius=r).set_stroke(DIM, 3).set_fill(BG, 0)
    s = 0.45 * r
    plus = VGroup(Line(LEFT * s, RIGHT * s), Line(DOWN * s, UP * s)).set_stroke(DIM, 3)
    return VGroup(ring, plus)


def lattice(cols=10, rows=4, pitch=(1.35, 1.2), r=0.3):
    """Regular grid of ions, centred on ORIGIN."""
    px, py = pitch
    g = VGroup(*[ion(r).move_to([(i - (cols - 1) / 2) * px, (j - (rows - 1) / 2) * py, 0])
                 for j in range(rows) for i in range(cols)])
    return g


def battery():
    """Vertical cell for the left-hand wire: long "+" plate on top, short "−" plate below, with
    leads spanning BAT_H. .plus_plate .minus_plate .plus_sign .minus_sign .leads"""
    long_p = Line(LEFT * 0.5, RIGHT * 0.5).shift(UP * 0.12).set_stroke(FG, 4)
    short_p = Line(LEFT * 0.25, RIGHT * 0.25).shift(DOWN * 0.12).set_stroke(FG, 9)
    leads = VGroup(Line(UP * 0.12, UP * BAT_H / 2), Line(DOWN * 0.12, DOWN * BAT_H / 2)).set_stroke(FG, WIRE_W)
    plus = T("+", 38).move_to([0.8, 0.3, 0])
    minus = T("−", 38).move_to([0.55, -0.32, 0])
    b = VGroup(leads, long_p, short_p, plus, minus)
    b.plus_plate, b.minus_plate, b.plus_sign, b.minus_sign, b.leads = long_p, short_p, plus, minus, leads
    return b


def lamp_glow(lamp_mob, color=YELLOW):
    """Soft glow rings behind a lamp (FadeIn it to light the lamp)."""
    c, r = lamp_mob.circle.get_center(), lamp_mob.circle.width / 2
    g = VGroup(*[Circle(radius=r + 0.08 * k).move_to(c).set_stroke(width=0).set_fill(color, 0.16)
                 for k in range(1, 6)])
    g.add(Circle(radius=r).move_to(c).set_stroke(width=0).set_fill(color, 0.35))
    g.set_z_index(-1)
    return g


def lamp(lit=False, r=0.42, span=SLOT_H):
    """Lamp for the right-hand slot: FG circle with an X, leads spanning `span`, centred on ORIGIN.
    lit=True adds the YELLOW glow. .circle .cross .leads .glow"""
    circ = Circle(radius=r).set_stroke(FG, 4).set_fill(BG, 1)
    d = r * 0.707
    cross = VGroup(Line([-d, -d, 0], [d, d, 0]), Line([-d, d, 0], [d, -d, 0])).set_stroke(FG, 4)
    leads = VGroup(Line(UP * r, UP * span / 2), Line(DOWN * r, DOWN * span / 2)).set_stroke(FG, WIRE_W)
    m = VGroup(leads, circ, cross)
    m.circle, m.cross, m.leads = circ, cross, leads
    m.glow = lamp_glow(m) if lit else VGroup()
    if lit:
        m.add_to_back(m.glow)
    return m


def resistor(label=None, vertical=True, span=SLOT_H, size=32):
    """FG rectangle with a lead each side spanning `span`, centred on ORIGIN; label (str or
    mobject) right of it (vertical) or above it (horizontal). .body .leads .label"""
    body = Rectangle(width=0.42, height=0.95).set_stroke(FG, 4).set_fill(BG, 1)
    leads = VGroup(Line(UP * 0.475, UP * span / 2), Line(DOWN * 0.475, DOWN * span / 2)).set_stroke(FG, WIRE_W)
    m = VGroup(leads, body)
    if not vertical:
        m.rotate(-PI / 2)
    lab = None
    if label is not None:
        lab = T(label, size) if isinstance(label, str) else label
        lab.next_to(body, RIGHT if vertical else UP, buff=0.22)
        m.add(lab)
    m.body, m.leads, m.label = body, leads, lab
    return m


def _tex_or_text(label, color, size):
    if not isinstance(label, str):
        return label.set_color(color)
    if any(ch in label for ch in "_\\^"):
        return MathTex(label, font_size=size * 1.25, color=color)
    return T(label, size, color)


def current_arrow(start, end, label=None, side=UP, size=30):
    """GOLD conventional-current arrow along a wire; optional GOLD label on `side`. .arrow .label"""
    a = Arrow(np.array(start), np.array(end), buff=0, stroke_width=5, color=GOLD,
              max_tip_length_to_length_ratio=0.35, tip_length=0.24)
    g = VGroup(a)
    g.arrow, g.label = a, None
    if label is not None:
        g.label = _tex_or_text(label, GOLD, size).next_to(a, side, buff=0.18)
        g.add(g.label)
    return g


def voltage_arrow(low, high, label=None, side=LEFT, size=32):
    """TEAL voltage arrow from the low end to the head at the higher potential; label in TEAL on
    `side` (str: MathTex if it has _ \\ ^, else serif). .arrow .label"""
    a = Arrow(np.array(low), np.array(high), buff=0, stroke_width=5, color=TEAL,
              max_tip_length_to_length_ratio=0.3, tip_length=0.24)
    g = VGroup(a)
    g.arrow, g.label = a, None
    if label is not None:
        g.label = _tex_or_text(label, TEAL, size).next_to(a, side, buff=0.2)
        g.add(g.label)
    return g


class Loop(VGroup):
    """p. 165's running loop: a rectangle of FG wire (LOOP_W × LOOP_H at LOOP_C), the battery in the
    middle of the left side ("+" up), an empty slot (filled by .slot_fill wire) in the middle of the
    right side. .wire = VGroup(lower, slot_fill, upper) .battery .slot_fill
    .point(u) / .normal(u): u in [0, 1) round the loop anticlockwise from the bottom-left corner
    (the electrons' direction); .slot_center(); .place(mob) moves mob into the slot;
    .corners() → (bl, br, tr, tl)."""

    def __init__(self):
        cx, cy = LOOP_C[0], LOOP_C[1]
        L, R, B, Tp = cx - LOOP_W / 2, cx + LOOP_W / 2, cy - LOOP_H / 2, cy + LOOP_H / 2
        lower = VMobject().set_points_as_corners([[L, cy - BAT_H / 2, 0], [L, B, 0], [R, B, 0],
                                                  [R, cy - SLOT_H / 2, 0]])
        upper = VMobject().set_points_as_corners([[R, cy + SLOT_H / 2, 0], [R, Tp, 0], [L, Tp, 0],
                                                  [L, cy + BAT_H / 2, 0]])
        fill = Line([R, cy - SLOT_H / 2, 0], [R, cy + SLOT_H / 2, 0])
        wire = VGroup(lower, fill, upper).set_stroke(FG, WIRE_W)
        bat = battery().move_to([L, cy, 0])
        bat.shift([L - bat.leads.get_x(), cy - bat.leads.get_y(), 0])
        super().__init__(wire, bat)
        self.wire, self.lower, self.upper, self.slot_fill, self.battery = wire, lower, upper, fill, bat

    def bounds(self):
        w = self.wire
        return w.get_left()[0], w.get_right()[0], w.get_bottom()[1], w.get_top()[1]

    def corners(self):
        L, R, B, Tp = self.bounds()
        return (np.array([L, B, 0]), np.array([R, B, 0]), np.array([R, Tp, 0]), np.array([L, Tp, 0]))

    def slot_center(self):
        L, R, B, Tp = self.bounds()
        return np.array([R, (B + Tp) / 2, 0])

    def battery_center(self):
        L, R, B, Tp = self.bounds()
        return np.array([L, (B + Tp) / 2, 0])

    def place(self, mob):
        return mob.move_to(self.slot_center())

    @staticmethod
    def _walk(u, bnd):
        L, R, B, Tp = bnd
        W, H = R - L, Tp - B
        s = (u % 1.0) * 2 * (W + H)
        if s < W:
            return np.array([L + s, B, 0]), DOWN
        s -= W
        if s < H:
            return np.array([R, B + s, 0]), RIGHT
        s -= H
        if s < W:
            return np.array([R - s, Tp, 0]), UP
        s -= W
        return np.array([L, Tp - s, 0]), LEFT

    def perimeter(self):
        L, R, B, Tp = self.bounds()
        return 2 * ((R - L) + (Tp - B))

    def point(self, u):
        return self._walk(u, self.bounds())[0]

    def normal(self, u):
        return self._walk(u, self.bounds())[1]


class LoopElectrons(VGroup):
    """LOOP_N electrons on a Loop's wire. Built at rest at their home slots ((i + 0.5)/n round the
    loop). .start() / .stop() the motion updater; trackers .drift (units/s, + = anticlockwise),
    .jitter (0 = still, 1 = full thermal jitter), .pos (accumulated drift). .motion(drift=, jitter=)
    → tracker animations; .snap() → animation that parks them back on home slots (with drift and
    jitter at 0)."""

    def __init__(self, loop, n=LOOP_N, seed=7, r=0.14):
        super().__init__(*[electron(r) for _ in range(n)])
        rng = np.random.default_rng(seed)
        self.loop, self.n = loop, n
        self.u0 = (np.arange(n) + 0.5) / n
        self.fa = rng.uniform(6, 10, (n, 2))
        self.ph = rng.uniform(0, TAU, (n, 4))
        self.drift, self.jitter, self.pos = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.clock = 0.0
        self.place_all()

    def place_all(self):
        bnd = self.loop.bounds()
        L, R, B, Tp = bnd
        P = 2 * ((R - L) + (Tp - B))
        j, t, off = self.jitter.get_value(), self.clock, self.pos.get_value() / P
        for i, e in enumerate(self.submobjects):
            f, ph = self.fa[i], self.ph[i]
            along = 0.24 * (0.6 * np.sin(f[0] * t + ph[0]) + 0.4 * np.sin(1.7 * f[1] * t + ph[1]))
            perp = 0.07 * (0.6 * np.sin(f[1] * t + ph[2]) + 0.4 * np.sin(1.9 * f[0] * t + ph[3]))
            p, nrm = Loop._walk(self.u0[i] + off + j * along / P, bnd)
            e.move_to(p + j * perp * nrm)

    def _step(self, m, dt):
        self.clock += dt
        if dt:
            self.pos.set_value(self.pos.get_value() + self.drift.get_value() * dt)
        self.place_all()

    def start(self):
        self.add_updater(self._step)
        return self

    def stop(self):
        self.remove_updater(self._step)
        return self

    def motion(self, drift=None, jitter=None):
        out = []
        if drift is not None:
            out.append(self.drift.animate.set_value(drift))
        if jitter is not None:
            out.append(self.jitter.animate.set_value(jitter))
        return out

    def snap(self):
        step = self.loop.perimeter() / self.n
        return self.pos.animate.set_value(round(self.pos.get_value() / step) * step)


# --- this scene's own pieces --------------------------------------------------------------
TUBE_Y, TUBE_R = 0.5, 0.55


def _tube(y=TUBE_Y, r=TUBE_R):
    return VGroup(Line([-7.05, y + r, 0], [7.05, y + r, 0]),
                  Line([-7.05, y - r, 0], [7.05, y - r, 0])).set_stroke(FG, 5)


def _edge_fade(e, x, edge=6.75, ramp=0.6, vis=1.0):
    """Electrons wrapping round the frame edge fade out and back in instead of being cut off.
    vis scales the whole opacity (a fade-in driven by a tracker, since this sets opacity directly)."""
    a = vis * float(np.clip((edge - abs(x)) / ramp, 0, 1))
    e[0].set_fill(opacity=a)
    e[1].set_stroke(opacity=a)


def opening_shot():
    """s1's last frame, this scene's first: the gate's output wire seen up close (a long FG tube),
    a YELLOW "?" in it, a GOLD "how much?" beside it. VGroup(tube, q, how)."""
    tube = _tube()
    q = T("?", 84, YELLOW).move_to([0, TUBE_Y, 0])
    how = T("how much?", 44, GOLD).move_to([2.6, TUBE_Y + TUBE_R + 0.55, 0])
    return VGroup(tube, q, how)


def handover_shot():
    """This scene's last frame, s3's first: the loop with its electrons at rest on their home
    slots. VGroup(loop, electrons): s3 does loop, els = shot; els.start(); then
    self.play(*els.motion(drift=DRIFT, jitter=1)) to set them drifting anticlockwise again."""
    loop = Loop()
    return VGroup(loop, LoopElectrons(loop))


DRIFT = 0.45   # loop drift speed, units/s (anticlockwise)


def wander(group, box, speed, seed, wrap_x=False):
    """Seeded random walk for every mob of group inside box (x0, x1, y0, y1); speed: a ValueTracker."""
    rng = np.random.default_rng(seed)
    n = len(group)
    a = rng.uniform(0, TAU, n)
    vel = np.stack([np.cos(a), np.sin(a)], 1)
    x0, x1, y0, y1 = box

    def upd(m, dt):
        s = speed.get_value()
        if dt == 0 or s <= 0:
            return
        vel[:] += rng.normal(0, 5.0 * np.sqrt(dt), (n, 2))
        vel[:] /= np.linalg.norm(vel, axis=1, keepdims=True)
        for i, e in enumerate(m.submobjects):
            x, y = e.get_x() + vel[i, 0] * s * dt, e.get_y() + vel[i, 1] * s * dt
            if wrap_x:
                if x > x1:
                    x -= x1 - x0
                elif x < x0:
                    x += x1 - x0
                _edge_fade(e, x)
            elif x < x0 or x > x1:
                x = 2 * (x0 if x < x0 else x1) - x
                vel[i, 0] *= -1
            if y < y0 or y > y1:
                y = 2 * (y0 if y < y0 else y1) - y
                vel[i, 1] *= -1
            e.move_to([x, y, 0])

    group.add_updater(upd)
    return upd


def _train(n=7, w=0.62, h=0.34, gap=0.2):
    cars = VGroup()
    for i in range(n):
        body = RoundedRectangle(corner_radius=0.06, width=w, height=h).set_stroke(BLUE, 3).set_fill(BLUE, 0.15)
        wheels = VGroup(*[Circle(radius=0.065).set_stroke(DIM, 2).set_fill(BG, 1)
                          .move_to(body.get_bottom() + [dx, 0, 0]) for dx in (-0.17, 0.17)])
        cars.add(VGroup(body, wheels).shift(RIGHT * i * (w + gap)))
    links = VGroup(*[Line(cars[i][0].get_right(), cars[i + 1][0].get_left()).set_stroke(FG, 2)
                     for i in range(n - 1)])
    return VGroup(cars, links)


def _compass(r=0.5):
    dial = Circle(radius=r).set_stroke(DIM, 3).set_fill(BG, 1)
    north = Polygon([0, 0.8 * r, 0], [0.12, 0, 0], [-0.12, 0, 0]).set_stroke(width=0).set_fill(RED, 1)
    south = Polygon([0, -0.8 * r, 0], [0.12, 0, 0], [-0.12, 0, 0]).set_stroke(width=0).set_fill(FG, 1)
    pin = Dot(radius=0.04, color=BG)
    needle = VGroup(north, south, pin)
    return VGroup(dial, needle)


class Electrons(NarratedScene):
    def construct(self):
        shot = opening_shot()
        self.add(shot)
        tube, q, how = shot
        self.clip1(tube, q, how)
        self.clip2(tube)
        loop, els = self.clip3(tube)
        self.clip4(loop, els)

    # ---- c6.metal.1: current = charges moving one way; metals vs gases ----------------------
    def clip1(self, tube, q, how):
        rng = np.random.default_rng(11)
        flow = VGroup(*[electron(0.14).move_to([-6.75 + 13.5 * (i + rng.uniform(0, 0.6)) / 16,
                                                TUBE_Y + rng.uniform(-0.3, 0.3), 0]) for i in range(16)])

        vis = ValueTracker(0.0)   # fade-in of the flow: frame 0 is exactly opening_shot()

        def run(m, dt):
            for e in m.submobjects:
                x = e.get_x() + 1.3 * dt
                x = x - 13.5 if x > 6.75 else x
                e.set_x(x)
                _edge_fade(e, x, vis=vis.get_value())
        for e in flow:
            _edge_fade(e, e.get_x(), vis=0.0)
        flow.add_updater(run)

        label = T("current: charged particles moving\nin a definite direction", 36,
                  t2c={"current:": YELLOW}, line_spacing=1.0).move_to([0, 2.45, 0])
        metals = T("metals: electrons", 34, t2c={"electrons": BLUE}).move_to([-3.6, -0.7, 0])

        jar = RoundedRectangle(corner_radius=0.3, width=2.7, height=2.0).set_stroke(DIM, 3)
        lid = Rectangle(width=1.5, height=0.16).set_stroke(width=0).set_fill(DIM, 1).next_to(jar, UP, buff=0.04)
        jar_g = VGroup(jar, lid).move_to([4.3, -2.25, 0])
        jr = np.random.default_rng(5)
        gas = VGroup(*[electron(0.12) for _ in range(6)], *[ion(0.24) for _ in range(3)])
        for p in gas:
            p.move_to(jar.get_center() + [jr.uniform(-0.95, 0.95), jr.uniform(-0.6, 0.6), 0])
        gas_speed = ValueTracker(1.3)
        jc = jar.get_center()
        wander(gas, (jc[0] - 1.05, jc[0] + 1.05, jc[1] - 0.7, jc[1] + 0.7), gas_speed, seed=9)
        gas_tag = T("gas or liquid:\nelectrons and ions", 34, t2c={"electrons": BLUE, "ions": DIM},
                    line_spacing=1.0)
        gas_tag.next_to(jar_g, LEFT, buff=0.5)

        with self.say("c6.metal.1") as c:
            self.add(flow)   # invisible (vis 0) until its fade
            self.play(*during(disappear(q, how), 0, 0.5), *during(vis.animate.set_value(1.0), 0.4, 1),
                      run_time=1.4)
            c.wait_until(own_word=label)
            self.play(*appear(label), run_time=1.0)
            c.wait_until("metals")
            self.play(*appear(metals), run_time=1.0)
            c.wait_until("gases")
            self.play(FadeIn(jar_g), FadeIn(gas), run_time=1.0)
            c.wait_until("liquid", own_word=gas_tag)
            self.play(*appear(gas_tag), run_time=1.0)
            c.wait_until("follow the electrons")
            self.play(*disappear(jar_g, gas, gas_tag), run_time=1.0)
            gas.clear_updaters()
        self.flow, self.label1, self.metals = flow, label, metals

    # ---- c6.metal.2: the lattice, random motion, no net flow ---------------------------------
    def clip2(self, tube):
        flow, label, metals = self.flow, self.label1, self.metals
        walls = VGroup(Line([-7.05, 2.4, 0], [7.05, 2.4, 0]), Line([-7.05, -2.4, 0], [7.05, -2.4, 0])).set_stroke(FG, 5)
        ions = lattice(10, 4, (1.35, 1.2), 0.3)
        rng = np.random.default_rng(21)
        els = VGroup()
        homes = []
        for k, io in enumerate(ions):
            a = rng.uniform(0, TAU)
            els.add(electron(0.13).move_to(io.get_center() + 0.44 * np.array([np.cos(a), np.sin(a), 0])))
            row = k // 10
            dx, dy = (0.675, 0.6) if row < 3 else (0.675, 0.0)
            homes.append(io.get_center() + [dx + rng.uniform(-0.15, 0.15), dy + rng.uniform(-0.12, 0.12), 0])
        speed = ValueTracker(0.0)

        check = DashedLine([0, -2.4, 0], [0, 2.4, 0], dash_length=0.12).set_stroke(YELLOW, 3)
        k = ValueTracker(0.0)

        def counter(direction, x, off):
            arr = Arrow(ORIGIN, direction * 0.6, buff=0, stroke_width=5, color=GOLD,
                        max_tip_length_to_length_ratio=0.4)
            num = always_redraw(lambda: T(str(int(k.get_value() + off)), 40, GOLD)
                                .next_to(arr, RIGHT, buff=0.2))
            g = VGroup(arr, num)
            arr.move_to([x - 0.3, 3.1, 0])
            return g
        left_c = counter(LEFT, -1.5, 0.5)
        right_c = counter(RIGHT, 1.1, 0.0)
        nonet = T("no net flow of charge, so no current", 36).move_to([0, -3.4, 0])

        with self.say("c6.metal.2", gap=1.0) as c:
            flow.clear_updaters()
            self.play(*during(disappear(label, metals, flow), 0, 0.4),
                      *during(Transform(tube, walls), 0.3, 1), run_time=min(2.0, c.until("its atoms")))
            c.wait_until("its atoms")
            self.play(LaggedStart(*[FadeIn(i) for i in ions], lag_ratio=0.03),
                      run_time=min(1.8, 0.8 * c.until("loose")))
            c.wait_until("loose")
            self.play(LaggedStart(*[FadeIn(e) for e in els], lag_ratio=0.02), run_time=1.2)
            self.add(els)   # the group itself on screen, so its wander updater runs
            c.wait_until("free to roam")
            self.play(*[e.animate.move_to(h) for e, h in zip(els, homes)],
                      run_time=min(1.8, 0.8 * c.until("random")))
            c.wait_until("at room temperature")
            wander(els, (-6.75, 6.75, -2.15, 2.15), speed, seed=4, wrap_x=True)
            self.play(speed.animate.set_value(3.2), run_time=1.2)
            c.wait_until("nonet")
            self.play(FadeIn(check), run_time=0.8)
            self.play(*appear(left_c, right_c, lag=0.0), run_time=0.8)   # early: counters, read as they tick
            self.play(k.animate.set_value(c.remaining * 1.6), run_time=c.until("no net flow"),
                      rate_func=linear)
            c.wait_until(own_word=nonet)
            self.play(*appear(nonet), k.animate.increment_value(2.4), run_time=1.5, rate_func=linear)
        self.c2 = (ions, els, check, left_c, right_c, nonet)

    # ---- c6.metal.3: the battery loop, pump, slow drift ---------------------------------------
    def clip3(self, tube):
        ions, els_l, check, left_c, right_c, nonet = self.c2
        loop = Loop()
        els = LoopElectrons(loop)
        pump = T("‘electron pump’", 36).next_to(loop.battery, RIGHT, buff=0.35)

        slow = T("< 1 mm per second", 40, GOLD).move_to([0.35, 0.75, 0])
        panel = Rectangle(width=5.0, height=2.4).set_stroke(DIM, 2).move_to([0, -1.1, 0])
        pions = VGroup(*[ion(0.26).move_to([x, y, 0]) for y in (-0.45, -1.75)
                         for x in (-1.9, -0.95, 0.0, 0.95, 1.9)])
        big = electron(0.2).move_to([2.25, -1.1, 0])
        zig = [2.25, 1.45, 1.75, 0.5, 0.8, -0.45, -0.15, -1.4, -1.1, -2.2]
        path = VMobject().set_points_as_corners(
            [[x, -1.1 if i == 0 else (-0.9 if i % 2 else -1.3), 0] for i, x in enumerate(zig)])
        inset = VGroup(panel, pions, big)

        L, R, B, Tp = loop.bounds()
        rl = Line([-3.0, Tp + 0.45, 0], [3.0, Tp + 0.45, 0]).set_stroke(DIM, 3)
        ticks = VGroup(*[Line([x, Tp + 0.45, 0], [x, Tp + 0.45 - (0.28 if i in (0, 10) else 0.14), 0])
                         for i, x in enumerate(np.linspace(-3.0, 3.0, 11))]).set_stroke(DIM, 3)
        ruler = VGroup(rl, ticks)
        one_m = T("1 m", 36, GOLD).next_to(rl, UP, buff=0.18)
        eq = VGroup(T("1 m ÷ 1 mm/s = 1000 s", 36, GOLD), T("over 15 minutes", 34, GOLD)).arrange(DOWN, buff=0.3)
        eq.move_to([0.35, -1.1, 0])

        with self.say("c6.metal.3") as c:
            els_l.clear_updaters()
            for m in (left_c, right_c):
                m[1].clear_updaters()
            c.wait_until("wire")
            self.play(*disappear(ions, els_l, check, left_c, right_c), run_time=0.8)
            c.wait_until("terminals")
            self.play(ReplacementTransform(tube, loop.wire), run_time=1.4)   # nonet stays below the loop
            self.play(*appear(loop.battery, shift=None), FadeIn(els), run_time=min(1.0, c.until("pump")))
            els.start()
            c.wait_until("pump")
            self.play(loop.battery.animate(rate_func=there_and_back).scale(1.2), *els.motion(jitter=1.0),
                      FlashAround(loop.battery, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until(own_word=pump)
            self.play(*appear(pump), *disappear(nonet), run_time=1.0)
            c.wait_until("it forces")
            self.play(*els.motion(drift=DRIFT), run_time=1.5)
            c.wait_until("positive terminal")
            self.play(FlashAround(loop.battery.plus_sign, run_time=1.5, time_width=1.5),
                      loop.battery.plus_sign.animate.set_color(YELLOW), run_time=1.5)
            c.wait_until("the drift is slow")
            self.play(*disappear(pump), loop.battery.plus_sign.animate.set_color(FG), run_time=0.8)
            c.wait_until("millimetre", own_word=slow)
            self.play(*appear(slow), run_time=1.0)
            c.wait_until("colliding")
            self.play(FadeIn(panel), LaggedStart(*[FadeIn(p) for p in pions], lag_ratio=0.05),
                      FadeIn(big), run_time=0.8)
            self.play(MoveAlongPath(big, path), rate_func=linear, run_time=max(0.5, c.until("at that speed") - 0.1))
            c.wait_until("at that speed")
            self.play(*disappear(inset), FadeIn(ruler), run_time=1.0)
            self.play(*appear(one_m), run_time=0.8)   # early: the metre the sentence is about
            c.wait_until("quarter", own_word=eq[0])
            self.play(*appear(eq[0], eq[1], lag=0.4), run_time=min(1.4, c.until()))
        self.c3 = (slow, ruler, one_m, eq)
        return loop, els

    # ---- c6.metal.4: all at once (train), heat and compass -------------------------------------
    def clip4(self, loop, els):
        slow, ruler, one_m, eq = self.c3
        bat = loop.battery
        train = _train().move_to([0.4, loop.bounds()[3] + 0.47, 0])
        box_w = 3.6
        L, R, B, Tp = loop.bounds()
        boxes = VGroup(*[DashedVMobject(RoundedRectangle(corner_radius=0.15, width=box_w, height=0.8),
                                        num_dashes=36).set_stroke(DIM, 2).move_to([x, Tp + 0.85, 0])
                         for x in (-2.1, 2.1)])
        warm = T("warmer", 32).move_to(boxes[0])
        comp_tag = T("compass def\u200clects", 32).move_to(boxes[1])   # ZWNJ: no "fl" ligature (read as "fi")
        glow = loop.wire.copy().set_stroke(HEAT, 18, opacity=0.25).set_z_index(-2)
        gclock = [0.0]

        def shimmer(m, dt):
            gclock[0] += dt
            m.set_stroke(opacity=0.22 + 0.1 * np.sin(7 * gclock[0]))
        compass = _compass().move_to([2.55, loop.slot_center()[1] + 0.5, 0])
        needle = compass[1]

        with self.say("c6.metal.4", gap=3.8) as c:
            self.play(bat.animate.shift(LEFT * 1.0), *els.motion(drift=0.0), run_time=1.2)
            c.wait_until("connected")
            self.play(bat.animate.shift(RIGHT * 1.0), run_time=0.5)
            els.drift.set_value(DRIFT)          # every electron starts on the same frame
            self.play(FlashAround(loop, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("how can that be")   # the slow-drift numbers stay up as the contrast to "and yet"
            self.play(*disappear(slow, ruler, one_m, eq), run_time=1.0)
            c.wait_until("every free electron")
            self.play(FadeIn(train), run_time=1.0)
            c.wait_until("like the carriages")
            self.play(train.animate.shift(LEFT * 0.6), run_time=1.2)
            c.wait_until("they all move")
            self.play(train.animate.shift(LEFT * 1.0), run_time=1.6)
            c.wait_until("shows")
            self.play(FadeOut(train), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3), run_time=1.0)
            c.wait_until("warm", own_word=warm)
            glow.add_updater(shimmer)
            self.play(FadeIn(glow), *appear(warm), run_time=0.9)
            c.wait_until("compass", own_word=comp_tag)
            self.play(FadeIn(compass), *appear(comp_tag), run_time=0.8)
            self.play(Rotate(needle, angle=-PI / 3, about_point=compass.get_center()), run_time=1.4)
        glow.clear_updaters()
        self.play(*disappear(boxes, warm, comp_tag, glow, compass), *els.motion(drift=0.0, jitter=0.0),
                  run_time=1.4)
        self.play(els.snap(), run_time=0.6)
        els.stop()
        self.wait(1.0)
