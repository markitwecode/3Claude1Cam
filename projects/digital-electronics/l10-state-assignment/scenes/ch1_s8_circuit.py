"""Chapter 1, scene 8: the binary divide-by-5 circuit built, run, scored; recap; next time. Clips c1.circuit.1 – c1.circuit.4.

Opens on s7's handover_shot() (three maps). The maps fade, their equations rise to a row at y 3.3,
and each flies to its gate. The circuit is ch2 s1's binary_circuit() (L6 make_ff / and_gate /
xor_gate), plus DIM chip numbers, an LED under each flip-flop, and a 1 Hz source.
Layouts (native circuit scaled about ORIGIN, then shifted): clip 1 L1 = 0.85 at (0.42, -0.71);
clip 2 L2 = 0.68 at (0.35, 0.61) with the CLK/Output plot (s5's divide5_wave) at y -2.75; from
{score} the circuit shrinks to L3 = 0.62 at (0.35, 0.95), ch2's scoreboard under it (top -1.4).
Recap: ch2_s8_recap's 3 x 2 grid. End: the circuit with its gates gone and a YELLOW "?", under
"Part 2 · More flip-flops, less logic", held ~8 s.
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
S4 = load_scene("ch1_s4_choice")
S5 = load_scene("ch1_s5_divide5")
S6 = load_scene("ch1_s6_count")
S7 = load_scene("ch1_s7_kmaps")
H2 = load_scene("ch2_s1_hook")
R2 = load_scene("ch2_s8_recap")


def _p(x, y):
    return np.array([x, y, 0.0])


def poly(pts, color, width=5):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


FF_X = H2.FF_X
CLK_Y = H2.CLK_Y
SCORE_ROW = ("binary", "3", "3", "none")
CHIPS = ("74HC08", "74HC86", "74HC08")
L1 = (0.85, _p(0.42, -0.71))
L2 = (0.68, _p(0.35, 0.61))
L4 = (0.85, _p(0.42, -0.95))
L3 = (0.62, _p(0.35, 0.95))     # from {score}: room for the scoreboard below
LED_ON, LED_OFF = (GREEN, 0.9), (BG, 0.0)


def lay(m, L):
    k, o = L
    return m.scale(k, about_point=ORIGIN).shift(o)


def build_rig():
    """The binary circuit, split into the pieces this scene shows one by one (native coords)."""
    circ = H2.binary_circuit()
    sub = circ.submobjects
    r = VGroup()
    r.circ = circ
    r.clk, r.dots, r.risers = sub[0], list(sub[1:3]), list(sub[3:6])
    r.ffs, r.names, r.gates = circ.ffs, circ.names, circ.gates
    gp = circ.gate_parts
    stubs, labels = list(gp[3:9]), list(gp[9:15])
    r.out_arrow, r.out_dot, r.out_l, r.clk_l = sub[13], sub[14], sub[15], sub[16]
    r.gate_center = circ.gate_center
    r.ff_chips = [T("74HC74", 30, DIM).move_to(_p(x - 0.35, 1.58)) for x in FF_X]   # just over the box
    r.g_chips = []
    for g, code in zip(r.gates, CHIPS):
        t = T(code, 34, DIM)
        t.move_to(_p(0, 2.7)).align_to(_p(g.out()[0] + 0.75, 0), LEFT)
        r.g_chips.append(t)
    r.in_labels = [labels[2 * i:2 * i + 2] for i in range(3)]
    r.gate_grps = [VGroup(r.gates[i], stubs[2 * i], stubs[2 * i + 1], *r.in_labels[i], r.risers[i])
                   for i in range(3)]
    r.leds = [R2.led(False).scale(1.25).move_to(_p(x + 0.72, -1.85)) for x in FF_X]
    sx = -5.6
    circle = Circle(radius=0.28).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(sx, -3.0))
    w = 0.13
    sq = poly([(-2 * w, -w), (-w, -w), (-w, w), (w, w), (w, -w), (2 * w, -w)], YELLOW, 3).move_to(circle)
    drop = Line(_p(sx, -2.72), _p(sx, CLK_Y)).set_stroke(YELLOW, 5)
    jd = Dot(_p(sx, CLK_Y), radius=0.08, color=YELLOW)
    r.src = VGroup(drop, jd, circle, sq)
    r.hz = T("1 Hz", 42, GOLD).next_to(circle, RIGHT, buff=0.15)
    r.bit_spots = [VectorizedPoint(_p(x, 0.0)) for x in FF_X]
    r.all = VGroup(r.clk, *r.dots, *r.ffs, *r.names, *r.gate_grps, r.out_arrow, r.out_dot, r.out_l,
                   r.clk_l, *r.ff_chips, *r.g_chips, *r.leds, r.src, r.hz, *r.bit_spots, r.gate_center)
    return r


def rings(mobs, color=GREEN):
    """A flash running once round each small label (a box round one glyph reads as an overbar)."""
    return [VShowPassingFlash(Circle(radius=max(m.width, m.height) / 2 + 0.14).move_to(m).set_stroke(color, 5),
                              time_width=1.0) for m in mobs]


def eq_drop(cp, body):
    """An equation's copy travels from its row down onto its gate and fades as the gate fades in."""
    a0, a1 = cp.get_center(), body[0].get_center()

    def upd(m, a):
        p = 1 - (1 - min(1.0, a / 0.7)) ** 2
        m.move_to(a0 + (a1 - a0) * p)
        op = 0.08 if p < 0.35 else min(1.0, 0.08 + (p - 0.35) / 0.15)
        m.set_opacity(op if a < 0.55 else max(0.0, 1 - (a - 0.55) / 0.3))
    return [UpdateFromAlphaFunc(cp, upd), FadeIn(body, rate_func=lambda t: smooth(max(0.0, (t - 0.55) / 0.45)))]


class Circuit(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ helpers
    def relayout(self, new_k, new_o):
        """MoveToTarget for the shown rig (self.R); the unshown pieces jump to the same layout."""
        k, o = self.lay
        s = new_k / k
        shift = new_o - s * o
        self.R.generate_target()
        self.R.target.scale(s, about_point=ORIGIN).shift(shift)
        shown = set(id(m) for m in self.R.get_family())
        for m in self.rig.all:
            for sm in m.get_family():
                if id(sm) not in shown and len(sm.submobjects) == 0:
                    shown.add(id(sm))
                    sm.scale(s, about_point=ORIGIN).shift(shift)
        self.lay = (new_k, new_o)
        return MoveToTarget(self.R)

    def clk_pulse(self, width=9):
        rig = self.rig
        paths = [rig.clk] + [f.clk_w for f in rig.ffs]
        return [VShowPassingFlash(m.copy().set_stroke(YELLOW, width), time_width=0.6) for m in paths]

    # ------------------------------------------------------------------ c1.circuit.1
    def clip1(self):
        shot = S7.handover_shot()
        self.add(shot)
        rig = self.rig = build_rig()
        lay(rig.all, L1)
        self.lay = L1
        eqs = [m.eq for m in shot]
        with self.say("c1.circuit.1") as c:
            # {ffs}: the maps go, their equations rise to a row; three flip-flops
            rest = [p for m in shot for p in m.submobjects if p is not m.eq]
            self.remove(shot)
            self.add(*rest, *eqs)
            eq_moves = [e.animate.set_y(3.3) for e in eqs]
            ffs_in = appear(*rig.ffs, lag=0.2) + appear(*rig.names, shift=None, lag=0.1)
            self.play(*during([FadeOut(p) for p in rest], 0, 0.4), *during(eq_moves, 0.3, 0.75),
                      *during(ffs_in, 0.45, 1.0), run_time=min(2.0, c.until("clk")))  # early: chip numbers aren't spoken
            self.eqs = eqs
            self.R = VGroup(*rig.ffs, *rig.names)
            settle(self, self.R)

            # {clk}: one clock line into every flip-flop
            c.wait_until("clk")
            self.play(Create(rig.clk, rate_func=linear), *[FadeIn(d) for d in rig.dots],
                      *appear(rig.clk_l, *rig.ff_chips, shift=None, lag=0.1),  # early: chip numbers aren't spoken
                      run_time=min(1.3, c.until("same clock")))
            settle(self, self.R, add=[rig.clk, *rig.dots, rig.clk_l, *rig.ff_chips])
            c.wait_until("same clock")
            self.play(*self.clk_pulse(), run_time=1.0)

            # {order}: a, b, c left to right; the table's c b a runs the other way
            c.wait_until("left to right")
            ffa, ffc = rig.ffs[0], rig.ffs[2]
            ay = 1.05
            c_arrow = Arrow(_p(ffa.get_x(), ay), _p(ffc.get_x(), ay), buff=0, color=GREEN, stroke_width=4,
                            tip_length=0.25, max_tip_length_to_length_ratio=0.1)
            c_lab = T("circuit", 30, DIM)
            c_lab.next_to(c_arrow, RIGHT, buff=0.25)
            self.play(GrowArrow(c_arrow), *appear(c_lab, shift=None),  # early: names the arrow being drawn
                      *rings(rig.names), run_time=1.6)
            c.wait_until("drew them")
            hx = 1.6
            head = VGroup(*[MathTex(t, font_size=42, color=GREEN).move_to(_p(hx + (j - 1) * 0.72, 2.3))
                            for j, t in enumerate("cba")])
            t_arrow = Arrow(_p(hx + 1.0, 1.85), _p(hx - 1.0, 1.85), buff=0, color=GREEN, stroke_width=4,
                            tip_length=0.25, max_tip_length_to_length_ratio=0.2)
            t_lab = T("table", 30, DIM).next_to(head, LEFT, buff=0.5).set_y(2.07)
            self.play(*appear(*head, lag=0.15), GrowArrow(t_arrow), *appear(t_lab, shift=None),  # early: the table's header, read on "table"
                      run_time=min(1.5, c.until("da")))
            order = [c_arrow, c_lab, *head, t_arrow, t_lab]

            # {da} {db} {dc}: each equation flies to its gate; its inputs and chip number follow
            cues = [("da", "inverted outputs", [ffa.qb_l, ffc.qb_l]),
                    ("db", "of a and bee", [rig.ffs[0].q_l, rig.ffs[1].q_l]),
                    ("dc", "of a and bee", [rig.ffs[0].q_l, rig.ffs[1].q_l])]
            for i, (cue, hit, srcs) in enumerate(cues):
                c.wait_until(cue)
                body = VGroup(*[m for m in rig.gate_grps[i] if m not in rig.in_labels[i]])
                out = during(disappear(*order), 0, 0.35) if i == 1 else []
                cp = eqs[i].copy()
                self.play(*out, *during(eq_drop(cp, body), 0.35 if i == 1 else 0, 1.0),
                          run_time=2.0 if i < 2 else 1.6)
                self.remove(cp)
                c.wait_until(hit, nth=1 if i == 2 else 0)
                self.play(*appear(*rig.in_labels[i], lag=0.2), *appear(rig.g_chips[i], shift=None),  # early: the chip number isn't spoken
                          *rings(srcs), run_time=1.2)
                settle(self, self.R, add=[body, *rig.in_labels[i], rig.g_chips[i]])

    # ------------------------------------------------------------------ c1.circuit.2
    def clip2(self):
        rig = self.rig
        with self.say("c1.circuit.2") as c:
            # {out}: the output is b's Q
            self.play(GrowArrow(rig.out_arrow), FadeIn(rig.out_dot), *appear(rig.out_l, shift=None),
                      *rings([rig.ffs[1].q_l]), run_time=1.2)
            settle(self, self.R, add=[rig.out_arrow, rig.out_dot, rig.out_l])

            # {run}: room for the plot; a 1 Hz source on the clock line
            c.wait_until("run")
            mv = self.relayout(*L2)
            self.play(*during(disappear(*self.eqs), 0, 0.35), *during([mv], 0.35, 1.0), run_time=1.6)
            c.wait_until("one hertz")
            self.play(FadeIn(rig.src), *appear(rig.hz, shift=None), *self.clk_pulse(7), run_time=1.0)
            settle(self, self.R, add=[rig.src, rig.hz])

            # the plot, hidden under a mask that slides right as time runs
            d5 = S5.divide5_wave(pattern=(0, 1, 1, 0, 0), label_size=44).scale(0.66)
            d5.move_to(_p(0, -2.75))
            self.d5 = d5
            body = VGroup(d5.guides, d5.clk, d5.out)
            x0 = d5.clk.wave.get_left()[0]
            x1 = d5.clk.wave.get_right()[0]
            rx = [d5.clk.rising_x(i) for i in range(10)]
            p = rx[1] - rx[0]
            mask = Rectangle(width=(x1 - x0) + 0.2, height=body.height + 0.3).set_stroke(width=0)
            mask.set_fill(BG, 1).set_z_index(5)
            mask.move_to(body).align_to(_p(x0 - 0.02, 0), LEFT)

            # {leds}: LEDs under each flip-flop; the circuit runs from 000
            c.wait_until("leds")
            self.add(body, mask)
            ro_at = rig.leds[2].get_right() + 0.3 * RIGHT

            def ro_text(v):
                return T(f"c b a = {v:03b}", 30, GREEN).move_to(ro_at, aligned_edge=LEFT)
            ro = ro_text(0)
            ro.v = 0
            self.play(*appear(*rig.leds, shift=None, lag=0.15), *appear(d5.clk_label, d5.out_label, ro, shift=None),
                      run_time=0.8)  # early: the plot's axis labels and the state readout
            settle(self, self.R, add=list(rig.leds))

            def led_upd(i):
                def upd(m):
                    n = sum(1 for x in rx if x < mask.get_left()[0] - 1e-3)
                    on = (n % 5 >> i) & 1
                    col, op = LED_ON if on else LED_OFF
                    m.set_fill(col, op).set_stroke(GREEN if on else DIM, 3)
                return upd
            for i, l in enumerate(rig.leds):
                l.add_updater(led_upd(i))

            def ro_upd(m):
                v = sum(1 for x in rx if x < mask.get_left()[0] - 1e-3) % 5
                if v != m.v:
                    m.become(ro_text(v))
                    m.v = v
            ro.add_updater(ro_upd)
            # count up through the five codes; the readout wraps to 000 on "zero zero zero"
            mr = mask.get_right()[0]
            self.play(mask.animate(rate_func=linear).stretch_to_fit_width(mr - rx[4] - 0.12 * p, about_edge=RIGHT),
                      run_time=c.until("zero zero zero", floor=1.0))

            # {high} two periods, {low} three
            c.wait_until("high")
            out_c = d5.out.get_center()[1]
            hgt = d5.out.height + 0.2

            def band(a, b, color):
                return (Rectangle(width=b - a, height=hgt).set_stroke(width=0).set_fill(color, 0.2)
                        .move_to(_p((a + b) / 2, out_c)).set_z_index(-2))
            hb = band(rx[1], rx[3], GREEN)
            h2 = T("2", 36, GOLD).move_to(hb)
            self.play(mask.animate(rate_func=linear).stretch_to_fit_width(mr - rx[6] - 0.02, about_edge=RIGHT),
                      *during([FadeIn(hb)] + appear(h2, shift=None), 0.4, 1.0),
                      run_time=c.until("low", floor=1.0))
            c.wait_until("low")
            lb = band(rx[3], rx[6], DIM)
            l3 = T("3", 36, GOLD).move_to(lb)
            self.play(FadeIn(lb), *appear(l3, shift=None), run_time=min(0.8, c.until("again")))

            # {again}: the rest runs; s5's waveform laid over it matches
            c.wait_until("again")
            ghost = S5.divide5_wave(pattern=(0, 1, 1, 0, 0), label_size=44).scale(0.66).move_to(d5).out
            ghost.set_stroke(GREEN, 14, opacity=0.3)
            rt = min(1.8, c.until("score") + 0.3)
            self.play(*during([mask.animate(rate_func=linear).stretch_to_fit_width(0.02, about_edge=RIGHT)], 0, 0.55),
                      *during(appear(ghost), 0.5, 1.0), run_time=rt)
            for l in (*rig.leds, ro):
                l.clear_updaters()
            self.remove(mask)

            # {score}: the scoreboard takes the plot's place
            c.wait_until("score")
            sb = H2.scoreboard([SCORE_ROW])
            sb.move_to(_p(0.35, 0)).align_to(_p(0, -1.4), UP)
            plot = [body, d5.clk_label, d5.out_label, hb, h2, lb, l3, ghost, ro]
            mv = self.relayout(*L3)
            self.play(*during(disappear(*plot), 0, 0.45), *during([mv], 0.2, 0.8),  # early: the scoreboard's column heads, read whole
                      *during(appear(sb.head, sb.rule, shift=None, lag=0.1), 0.5, 1.0), run_time=1.6)

            # {row}: binary | 3 | 3 | none
            c.wait_until("binary")
            cells = list(sb.rows[0])
            self.play(*appear(cells[0], shift=None), run_time=0.7)
            for cell, cue in zip(cells[1:], ("three flip-flops", "three gates", "no output")):
                c.wait_until(cue)
                self.play(*appear(cell, shift=None), run_time=0.7)

    # ------------------------------------------------------------------ c1.circuit.3: recap
    def clip3(self):
        self.panels = []
        with self.say("c1.circuit.3") as c:
            head = T("Recap", 40).move_to(_p(0, 3.4))
            frames = [R2.slot_frame(i) for i in range(6)]
            self.play(*during([FadeOut(m) for m in self.mobjects], 0, 0.45),
                      *during(appear(head, shift=None) + [FadeIn(f) for f in frames], 0.5, 1.0),
                      run_time=min(1.5, c.until("r1")))  # early: the scene's heading

            def panel(i, vis, lines, cue, word_cue, **kw):
                c.wait_until(cue)
                cap = R2.caption(i, lines, **kw) if lines and isinstance(lines[0], str) else lines_group(i, lines)
                self.play(*self.dim_previous(), FadeIn(vis), run_time=0.9)  # early: the panel's picture, shown whole
                c.wait_until(word_cue)
                self.play(*appear(cap, shift=None), run_time=min(0.9, max(0.4, c.until(None) - 0.1)))
                self.panels.append(VGroup(vis, cap))

            def lines_group(i, rows):
                x, top = R2.slot(i)
                g = VGroup(*rows).arrange(DOWN, buff=0.1)
                return g.move_to(_p(x, 0)).align_to(_p(0, top - 2.3), UP)

            # r1: the traffic-light ring with its codes
            ring = S1.traffic_ring(["100", "110", "001", "010"], code_size=44)
            R2.fit(ring, R2.vis_center(0))
            panel(0, ring, ["a pattern of bits", "for each state"], "r1", "pattern")

            # r2: the doubling ladder and the ceiling of log2 m
            lad = S4.doubling_ladder(with_formula=True)
            R2.fit(lad, R2.vis_center(1))
            row2 = VGroup(MathTex(r"\lceil \log_2 m \rceil", font_size=36), T("flip-flops", 28)).arrange(RIGHT, buff=0.15)
            panel(1, lad, [T("m states:", 28, slant=ITALIC), row2], "r2", "log base two")

            # r3: s5's waveform under its GOLD ÷ 5
            wave = S5.divide5_wave()
            div = MathTex(r"\div\,5", font_size=72, color=GOLD).next_to(wave, UP, buff=0.35)
            v3 = VGroup(wave, div)
            R2.fit(v3, R2.vis_center(2))
            panel(2, v3, ["5 states:", "3 flip-flops"], "r3", "needs three", t2c={"5": GOLD, "3": GOLD})

            # r4: s6's table, b's column boxed
            tab = S6.count_table(boxed=True)
            R2.fit(tab, R2.vis_center(3))
            panel(3, tab, ["output = b"], "r4", "came free", t2c={"b": GREEN})

            # r5: s7's three maps with their loops
            maps = S7.compare_maps()
            R2.fit(maps, R2.vis_center(4))
            panel(4, maps, ["unused states", "as don't cares"], "r5", "don't cares")

            # r6: this scene's circuit and its scoreboard row
            circ = H2.binary_circuit()
            sbm = H2.scoreboard([SCORE_ROW], n_rows=1)
            vc = R2.vis_center(5)
            R2.fit(circ, vc + 0.32 * UP, h=1.45)
            R2.fit(sbm, vc + 0.82 * DOWN, h=0.62)
            panel(5, VGroup(circ, sbm), ["3 flip-flops, 3 gates"], "r6", "three gates", t2c={"3": GOLD})

    def dim_previous(self):
        out = []
        for t in self.panels:
            if not getattr(t, "veiled", False):
                t.veiled = True
                out.append(FadeIn(R2.veil(t)))
        return out

    # ------------------------------------------------------------------ c1.circuit.4: next time
    def clip4(self):
        with self.say("c1.circuit.4") as c:
            # {next}: the panels clear; the circuit returns alone
            c.wait_until("built on")
            rig = build_rig()
            lay(rig.all, L4)
            gates = [VGroup(g.submobjects[0], *g.submobjects[1:5]) for g in rig.gate_grps]
            circ = VGroup(rig.clk, *rig.dots, *rig.ffs, *rig.names, *rig.gate_grps, rig.out_arrow, rig.out_dot,
                          rig.out_l, rig.clk_l)
            self.play(*during([FadeOut(m) for m in self.mobjects], 0, 0.45), *during([FadeIn(circ)], 0.5, 1.0),
                      run_time=1.5)

            # a GOLD 1 hops from flip-flop to flip-flop, as in a shift register
            c.wait_until("shift register")
            one = T("1", 48, GOLD).move_to(rig.bit_spots[0])
            self.play(*appear(one, shift=None), run_time=0.5)
            hop = max(0.5, min(0.8, (c.until("vanish") - 0.9) / 2))
            for k in (1, 2):
                self.play(one.animate.move_to(rig.bit_spots[k]), run_time=hop)
                if k == 1:
                    self.wait(0.45)   # the 1 rests on b before moving on

            # {vanish}: the gates fade one by one; a "?" where the logic was
            c.wait_until("vanish")
            self.remove(circ)
            keep = [m for m in circ if m not in rig.gate_grps]
            parts = [m for g in rig.gate_grps for m in g.submobjects]
            self.add(*keep, *parts)
            outs = []
            for i, g in enumerate(gates):
                outs += [time_span(FadeOut(m), 0.55 * i, 0.55 * i + 0.8) for m in g.submobjects]
            self.play(*outs, run_time=1.9)
            c.wait_until("almost disappears")
            q = T("?", 96, YELLOW).move_to(rig.gate_center)
            self.play(*appear(q, shift=None), run_time=min(1.0, c.until(floor=0.6)))

        # end card: next part's title over the vanished logic, held ~8 s
        nxt = T("Part 2 · More flip-flops, less logic", 40).move_to(_p(0, 3.35))
        self.play(*appear(nxt), run_time=1.2)  # early: the end card's title
        self.wait(7.0)
