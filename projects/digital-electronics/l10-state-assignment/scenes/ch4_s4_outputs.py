"""Chapter 4, scene 4: lighting the lamps: OR the flip-flop outputs (p. 138), then p. 139's whole
one-hot circuit. Clips c4.lamps.1 – c4.lamps.3.

Chapter-wide helper owned here (s5 – s8 import it via load_scene("ch4_s4_outputs")):
- onehot_circuit(bits="1000") -> VGroup, p. 139's circuit at full size (about 12.4 x 6.2, x -6.0..5.6,
  y -2.75..3.0): s3's ring4 with its box centres at y = 1.25 (R4_Y), D_r D_ra D_g D_a (BLUE MathTex)
  over the D input stubs, Q taps (junction dots) on the wires between the flip-flops, the OR gate
  for R (fed by Q_r, Q_ra) and for A (fed by Q_ra, Q_a), G a straight wire down from Q_g, and
  three lamps R A G (dark discs, labels in the lamp colours) underneath.
  Attributes: .ring (ring4: .step() etc.), .dsubs[i], .gates[0/1] (ch2 s1 Gate, pointing down),
  .in_wires[0/1] (the two input wires of each gate), .out_wires[0/1] (gate -> lamp), .g_wire,
  .dots, .lamps[k] (discs), .lamp_labels[k], .lamp_units[k] = VGroup(disc, label) for k = R, A, G.
  .light(state) -> list of anims lighting the lamps of state 0-3 (red, red+amber, green, amber)
  and darkening the rest; light(None) darkens all. Shift/scale the whole group freely.
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

S1 = load_scene("ch1_s1_hook")
S21 = load_scene("ch2_s1_hook")
S2 = load_scene("ch4_s2_onehot")
S3 = load_scene("ch4_s3_ring4")

LAMP_COLS = (S1.LAMP_RED, S1.LAMP_AMBER, S1.LAMP_GREEN)
NAMES = S3.NAMES


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- onehot_circuit (chapter-wide) ------------------------------------------------------------------
PIN = S3.R4_Y + S21.PIN_Y * S3.R4_S      # 1.61: the Q -> D wires
BUS_Y = -0.6                              # horizontal feeds to the gates
GATE_Y = -1.45
LAMP_Y = -2.55
LAMP_R = 0.36
TAP_X = (-2.9, -0.15, 2.85, 5.35)        # where Q_r, Q_ra, Q_g, Q_a are tapped
GATE_X = (-0.65, 1.35)                     # OR for R, OR for A
LAMP_X = (-0.65, 1.35, 2.85)               # lamps R, A, G
LAMP_ON = [(1, 0, 0), (1, 1, 0), (0, 0, 1), (0, 1, 0)]    # R A G per state r ra g a


def _wire(*pts):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(FG, 4)


def or_gate():
    g = S21.Gate(S21._or_body(), [(-0.71, 0.3), (-0.71, -0.3)], (0.7, 0.0), color=BLUE)
    return g.rotate(-PI / 2).scale(0.85)


def onehot_circuit(bits="1000"):
    C = VGroup()
    R = S3.ring4(bits).shift(S3.R4_Y * UP)
    dsubs = []
    for i, ff in enumerate(R.ffs):
        d = MathTex("D_{" + NAMES[i] + "}", font_size=32, color=BLUE)
        d.next_to(ff.d_w, UP, buff=0.06)
        d.shift((ff.box.get_left()[0] - 0.07 - d.get_right()[0]) * RIGHT)
        dsubs.append(d)
    gates = [or_gate().move_to(_p(x, GATE_Y)) for x in GATE_X]

    def ins(g):
        a, b = g.inp(0), g.inp(1)
        return (a, b) if a[0] < b[0] else (b, a)

    (rl, rr), (al, ar) = ins(gates[0]), ins(gates[1])
    top = LAMP_Y + LAMP_R
    tr, tra, tg, ta = TAP_X
    w_r = _wire((tr, PIN), (tr, BUS_Y), (rl[0], BUS_Y), (rl[0], rl[1]))
    w_ra_r = _wire((tra, PIN), (tra, BUS_Y), (rr[0], BUS_Y), (rr[0], rr[1]))
    w_ra_a = _wire((tra, BUS_Y), (al[0], BUS_Y), (al[0], al[1]))
    w_a = _wire((ta, PIN), (ta, BUS_Y), (ar[0], BUS_Y), (ar[0], ar[1]))
    outs = [_wire((g.out()[0], g.out()[1]), (g.out()[0], top)) for g in gates]
    g_wire = _wire((tg, PIN), (tg, top))
    dots = [Dot(_p(x, PIN), radius=0.075, color=FG) for x in TAP_X] + [Dot(_p(tra, BUS_Y), radius=0.075, color=FG)]
    lamps, labels, units = [], [], []
    for k, ch in enumerate("RAG"):
        disc = Circle(radius=LAMP_R).set_stroke(DIM, 2).set_fill(S1.LAMP_OFF, 1).move_to(_p(LAMP_X[k], LAMP_Y))
        lab = T(ch, 36, LAMP_COLS[k]).next_to(disc, RIGHT, buff=0.15)
        lamps.append(disc)
        labels.append(lab)
        units.append(VGroup(disc, lab))
    C.add(R, *dsubs, w_r, w_ra_r, w_ra_a, w_a, *outs, g_wire, *dots, *gates, *units)
    C.ring, C.dsubs, C.gates = R, dsubs, gates
    C.in_wires, C.out_wires, C.g_wire, C.dots = [[w_r, w_ra_r], [w_ra_a, w_a]], outs, g_wire, dots
    C.lamps, C.lamp_labels, C.lamp_units = lamps, labels, units

    def light(state):
        on = (0, 0, 0) if state is None else LAMP_ON[state]
        return [lamps[k].animate.set_fill(LAMP_COLS[k] if on[k] else S1.LAMP_OFF, 1) for k in range(3)]

    C.light = light
    return C


# ---- this scene -------------------------------------------------------------------------------------
EQ_Y = -3.45


def out_eq(name, col, *terms):
    parts = [name, "="]
    for k, t in enumerate(terms):
        if k:
            parts.append("+")
        parts.append(t)
    m = MathTex(*parts, font_size=44)
    m[0].set_color(col)
    for k in range(2, len(parts), 2):
        m[k].set_color(GREEN)
    return m


def slide_step(scene, R, run_time=0.8, extra=()):
    """R.step, but the 1 itself slides along the wire into the next cell (one move, so the 1 is
    always visible): the next cell's 0 fades out first, the left cell's new 0 fades in after."""
    i = R.values.index(1)
    j = (i + 1) % 4
    one, old_j = R.bits[i], R.bits[j]
    new_i = S3.cell_bit(0, S3.R4_BIT).move_to(R.bit_pos(i))
    ti, tj = R.cells[i].copy(), R.cells[j].copy()
    S3.ring_cell_style(ti, 0)
    S3.ring_cell_style(tj, 1)
    p = R.wire_paths[i].copy().move_to(R.wires[i]).set_stroke(GOLD, 7)
    scene.play(*during(disappear(old_j), 0, 0.35), *during([one.animate.move_to(R.bit_pos(j))], 0.05, 0.9),
               *during(appear(new_i, shift=None), 0.6, 1.0), Transform(R.cells[i], ti), Transform(R.cells[j], tj),
               VShowPassingFlash(p, time_width=0.6, taper_width=0.1), *extra, run_time=run_time)
    R.values[i], R.values[j] = 0, 1
    R.bits[i], R.bits[j] = new_i, one
    settle(scene, R, add=[new_i], drop=[old_j])


def dense_path(path, step=0.08):
    """The same corner path, resampled into short equal pieces, so a VShowPassingFlash travels it at
    an even speed (a plain corner path gives each segment, long or short, the same share of time)."""
    pts = path.get_anchors()
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(1, int(np.linalg.norm(b - a) / step))
        out += [a + (b - a) * k / n for k in range(1, n + 1)]
    q = []
    for p in out:
        if not q or np.linalg.norm(p - q[-1]) > 1e-6:
            q.append(p)
    return VMobject().set_points_as_corners(q).set_stroke(path.get_stroke_color(), path.get_stroke_width())


def ring_track(ring, i, j, n=40):
    """Clockwise quarter of the ring's inner ellipse from ring.inner(i) to ring.inner(j)."""
    h = ring._hub.get_center()
    ax = np.linalg.norm(ring.inner(1) - h)
    ay = np.linalg.norm(ring.inner(0) - h)
    ang = {0: PI / 2, 1: 0.0, 2: -PI / 2, 3: -PI}
    a0 = ang[i]
    a1 = a0 - PI / 2
    ts = np.linspace(a0, a1, n)
    return VMobject().set_points_smoothly([h + np.array([ax * np.cos(t), ay * np.sin(t), 0]) for t in ts])


def dashed_box(x0, x1, y0, y1, color):
    r = Rectangle(width=x1 - x0, height=y1 - y0).move_to(_p((x0 + x1) / 2, (y0 + y1) / 2))
    return DashedVMobject(r.set_stroke(color, 3), num_dashes=60, dashed_ratio=0.55)


class Outputs(NarratedScene):
    def construct(self):
        shot = S3.handover_shot()
        self.R, self.ring, self.codes = shot[0], shot[1], list(shot[2:])
        self.add(self.R, self.ring, *self.codes)
        self.C = onehot_circuit()
        eqs = [out_eq("R", LAMP_COLS[0], "r", "ra"), out_eq("A", LAMP_COLS[1], "ra", "a"),
               out_eq("G", LAMP_COLS[2], "g")]
        VGroup(*eqs).arrange(RIGHT, buff=1.0)
        VGroup(*eqs).shift(_p(LAMP_X[0] - eqs[0].get_x(), EQ_Y - eqs[0].get_y()))
        self.eqs = eqs
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(3.4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # helpers
    def glow(self, states):
        """Spotlight states (ring circles + cell labels) in YELLOW; the others back to normal."""
        anims = []
        for i in range(4):
            on = i in states
            anims.append(restyle(self.ring.circles[i], outline=YELLOW if on else BLUE, width=6 if on else 4))
            anims.append(self.R.labels[i].animate.set_color(YELLOW if on else GREEN))
        anims += [FlashAround(self.R.cells[i], color=YELLOW, time_width=1.5) for i in states]
        return anims

    def unglow(self):
        anims = []
        for i in range(4):
            anims.append(restyle(self.ring.circles[i], outline=BLUE, width=4))
            anims.append(self.R.labels[i].animate.set_color(GREEN))
        return anims

    # ------------------------------------------------------------------------------------ c4.lamps.1
    def clip1(self):
        R, ring, C = self.R, self.ring, self.C
        tag = T("4 flip-flops, 3 lamps", 36, FG, t2c={"4": GOLD, "3": GOLD}).move_to(_p(1.1, -1.3))
        self.tag = tag
        with self.say("c4.lamps.1") as c:
            c.wait_until("now say")
            self.play(FlashAround(R.cells[0], color=GOLD, time_width=1.5), S3.ring_flash(ring.circles[0]),
                      run_time=1.2)
            c.wait_until("four flip-flops")
            self.play(*[time_span(FlashAround(R.cells[i], color=YELLOW, time_width=1.5), 0.2 * i, 0.2 * i + 1.0)
                        for i in range(4)], run_time=1.6)
            c.wait_until("three lamps")
            self.play(*appear(*C.lamp_units, lag=0.2), run_time=1.2)  # early: the lamps, named as a set
            self.play(*appear(tag), run_time=1.0)

            c.wait_until("red")
            self.play(*self.glow([0, 1]), run_time=1.2)
            c.wait_until("either the red")
            self.play(Create(C.in_wires[0][0]), FadeIn(C.dots[0], scale=0.5), run_time=1.5)
            c.wait_until("or the red-and-amber")
            self.play(Create(C.in_wires[0][1]), FadeIn(C.dots[1], scale=0.5), run_time=1.5)

            c.wait_until("redor")
            self.play(*during(disappear(tag), 0, 0.4), *during([FadeIn(C.gates[0], scale=0.8)], 0.3, 0.75),
                      *during([Create(C.out_wires[0])], 0.65, 1.0), run_time=min(1.3, c.until() - 1.0))
            self.play(*appear(self.eqs[0]), *self.unglow(), run_time=min(1.0, max(0.6, c.until() - 0.05)))

    # ------------------------------------------------------------------------------------ c4.lamps.2
    def clip2(self):
        R, ring, C, eqs = self.R, self.ring, self.C, self.eqs
        with self.say("c4.lamps.2") as c:
            self.play(*self.glow([1, 3]), run_time=1.2)
            c.wait_until("amberor")
            self.play(Create(C.in_wires[1][0]), Create(C.in_wires[1][1]), FadeIn(C.dots[3], scale=0.5),
                      FadeIn(C.dots[4], scale=0.5), run_time=1.4)
            self.play(*during([FadeIn(C.gates[1], scale=0.8)], 0, 0.5), *during([Create(C.out_wires[1])], 0.4, 0.75),
                      *during(appear(eqs[1]), 0.55, 1.0), run_time=min(1.6, c.until("green") - 0.1))

            c.wait_until("green")
            self.play(*self.glow([2]), run_time=1.2)
            c.wait_until("simply")
            self.play(Create(C.g_wire), FadeIn(C.dots[2], scale=0.5), run_time=1.5)
            self.play(*appear(eqs[2]), *self.unglow(), run_time=1.0)

            c.wait_until("rule")
            b = S2.bullet(["Outputs are generated by", "ORing together appropriate", "FF outputs"], 28)
            b.move_to(_p(-4.0, -2.0)).align_to(_p(-6.5, 0), LEFT)
            self.bullet = b
            self.play(*during(disappear(ring, *self.codes), 0, 0.45),
                      *during(appear(b, shift=None), 0.5, 1.0), run_time=1.4)  # early: the slide's bullet, the rule it names
            self.play(FlashAround(b, color=YELLOW, time_width=1.5), *[l.animate.set_color(YELLOW) for l in b.lines],
                      run_time=1.4)
            c.wait_until("each output")
            self.play(*flash(eqs, color=YELLOW, time_width=1.5), run_time=1.5)

    # ------------------------------------------------------------------------------------ c4.lamps.3
    def clip3(self):
        R, ring, C = self.R, self.ring, self.C
        with self.say("c4.lamps.3") as c:
            self.play(*disappear(*self.eqs), *set_alpha([self.bullet], 0.5), run_time=1.2)
            c.wait_until("four dee")
            self.play(*appear(*C.dsubs, lag=0.15), run_time=1.3)
            c.wait_until("one clock")
            clk = R.clk_line.copy().set_stroke(YELLOW, 9)
            self.play(VShowPassingFlash(clk, time_width=0.6, taper_width=0.1),
                      FlashAround(R.clk_label, color=YELLOW, time_width=1.5), run_time=1.5)

            c.wait_until("each output is wired")
            flashes = []
            for i in range(3):
                p = R.wire_paths[i].copy().move_to(R.wires[i]).set_stroke(GOLD, 8)
                flashes.append(time_span(VShowPassingFlash(p, time_width=0.8, taper_width=0.1), 0.4 * i, 0.4 * i + 0.9))
            self.play(*flashes, run_time=1.7)
            c.wait_until("runs back")
            p = dense_path(R.wire_paths[3].copy().move_to(R.wires[3]).set_stroke(GOLD, 9))
            self.play(VShowPassingFlash(p, time_width=0.35, taper_width=0.1), FlashAround(R.cells[0], color=GOLD, time_width=1.5),
                      run_time=min(2.0, c.until("ors") - 0.1), rate_func=linear)

            c.wait_until("ors")
            g_path = C.g_wire.copy().set_stroke(LAMP_COLS[2], 9)
            self.play(*flash(C.gates, color=YELLOW, time_width=1.5),
                      VShowPassingFlash(g_path, time_width=0.6, taper_width=0.1), run_time=1.5)

            # ---- run: the 1 goes round, the lamps follow
            c.wait_until("run")
            dot = Dot(ring.inner(0), radius=0.08, color=YELLOW)
            self.play(*during(disappear(self.bullet), 0, 0.45),
                      *during([*appear(ring, *self.codes, shift=None), FadeIn(dot, scale=0.5)], 0.5, 1.0),
                      run_time=min(1.4, c.until("red") - 0.05))
            c.wait_until("red")
            self.play(*C.light(0), S3.ring_flash(ring.circles[0]), FlashAround(R.cells[0], color=GOLD), run_time=0.8)
            for j, cue in [(1, "then red and amber"), (2, "then green"), (3, "then amber")]:
                c.wait_until(cue)
                slide_step(self, R, run_time=1.0, extra=[MoveAlongPath(dot, ring_track(ring, j - 1, j)), S3.ring_flash(ring.circles[j]),
                                                       *C.light(j)])

            # ---- what's left of the logic
            c.wait_until("logic")
            ff_box = dashed_box(-5.32, 5.2, 0.3, 2.75, BLUE)
            ff_tag = T("next-state logic: none", 32, FG, t2c={"none": GREEN})
            ff_tag.move_to(_p(0, -1.1)).align_to(_p(-6.4, 0), LEFT)
            self.play(*during(disappear(ring, *self.codes, dot), 0, 0.45),
                      *during([FadeIn(ff_box)], 0.4, 0.8), *during(appear(ff_tag), 0.5, 1.0), run_time=1.5)
            c.wait_until("output logic")
            g0, g1 = C.gates
            or_box = dashed_box(g0.get_left()[0] - 0.15, g1.get_right()[0] + 0.15, -2.12, -0.72, GOLD)
            or_tag = T("output logic: 2 OR gates", 30, FG, t2c={"2": GOLD})
            or_tag.move_to(_p(0, -2.3)).align_to(_p(-6.4, 0), LEFT)
            self.play(FadeIn(or_box), *during(appear(or_tag), 0.3, 1.0), run_time=1.3)
