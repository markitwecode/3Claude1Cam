"""Chapter 5, scene 6: climb the Hermite ladder to H_3 and H_4, the notes' typo, the oscillator plots.
Clips c5.ladder.1 – c5.ladder.4.

Opens on ch5_s5's handover_shot() (def line, ladder_card(3), boxed recursion). On {climb} the def line
goes, the boxed recursion rises to the top of the work area and the ladder moves to the left edge
(scale 1.05). Work rows right of it, first "=" at x = X_EQ. Clip 2: the notes' box (p63) replaces the
recursion at the top; parity tags right of the rungs. Clip 3: H_4 in rows under the inset. Clip 4: the
ladder slides further left, osc_plots() fill the right. Ends on an empty frame.

Exports: osc_plots() (for the recap).
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403


def _s2():
    return load_scene("ch5_s2_define")


# ---------------------------------------------------------------- layout
L_SCALE, L_CENTER = 1.05, np.array([-4.5, -0.85, 0])     # ladder at the left (clips 1-3)
L2_SCALE, L2_CENTER = 0.88, np.array([-4.95, -0.7, 0])   # clip 4: slid further left
BOX_TOP = np.array([2.2, 3.05, 0])                      # boxed recursion, top of the work area
X_EQ = 0.6                                              # first "=" of the work rows
TAG_X = -2.25                                           # left edge of the parity tags
EVEN_C, ODD_C = FG, YELLOW


def _place(m, scale=L_SCALE, center=L_CENTER):
    """Put a mobject built in s2's card coordinates into the moved ladder."""
    c0 = _s2().LADDER_CENTER
    return m.scale(scale, about_point=c0).shift(center - c0)


def mrow(parts, size=44, yellow=("H_",)):
    m = MathTex(*parts, font_size=size, color=FG)
    for i, p in enumerate(parts):
        if any(p.startswith(y) for y in yellow):
            m[i].set_color(YELLOW)
    return m


def _at_eq(m, eq_idx, y, x_eq=X_EQ):
    m.shift(np.array([x_eq - m[eq_idx].get_center()[0], y - m[eq_idx].get_center()[1], 0]))
    return m


# ---------------------------------------------------------------- the oscillator plots (exported)
OSC_H = [lambda x: 1.0 + 0 * x, lambda x: 2 * x, lambda x: 4 * x * x - 2, lambda x: 8 * x ** 3 - 12 * x]
OSC_ZEROS = [[], [0.0], [-1 / np.sqrt(2), 1 / np.sqrt(2)], [-np.sqrt(1.5), 0.0, np.sqrt(1.5)]]
OSC_CX, OSC_Y0, OSC_PITCH, OSC_AMP, OSC_SX = 2.2, -2.55, 1.5, 0.55, 1.0


def osc_plots():
    """Four stacked oscillator states H_n(x) e^{-x^2/2}, n = 0..3 bottom-up (as ch5_s1's preview:
    BLUE curves, each scaled to the same height 0.55, DIM base line, x from -4 to 4).
    VGroup(*rows, caption); .rows[n] = VGroup(base, curve, label) with .base .curve .label
    (MathTex "n = k" 34) and .dots (YELLOW zero crossings, not in the group: add them yourself);
    .caption = MathTex 44 H_n(x) e^{-x^2/2} (gauss PURPLE) above the plots. Spans x -2.8..6.2,
    y -2.6..3.6."""
    g = VGroup()
    g.rows = []
    xs = np.linspace(-4, 4, 801)
    for n, h in enumerate(OSC_H):
        amp = np.max(np.abs(h(xs) * np.exp(-xs * xs / 2)))
        y0 = OSC_Y0 + OSC_PITCH * n
        base = Line([OSC_CX - 4 * OSC_SX, y0, 0], [OSC_CX + 4 * OSC_SX, y0, 0], stroke_color=DIM, stroke_width=2)
        curve = FunctionGraph(
            lambda x, h=h, amp=amp, y0=y0: y0 + OSC_AMP * h((x - OSC_CX) / OSC_SX)
            * np.exp(-((x - OSC_CX) / OSC_SX) ** 2 / 2) / amp,
            x_range=[OSC_CX - 4 * OSC_SX, OSC_CX + 4 * OSC_SX, 0.02], color=BLUE)
        curve.set_stroke(width=4)
        label = MathTex(f"n = {n}", font_size=34, color=FG)
        label[0][-1].set_color(GOLD)
        label.next_to(base, LEFT, buff=0.3)
        row = VGroup(base, curve, label)
        row.base, row.curve, row.label = base, curve, label
        row.dots = VGroup(*[Dot([OSC_CX + z * OSC_SX, y0, 0], radius=0.09, color=YELLOW).set_z_index(2)
                            for z in OSC_ZEROS[n]])
        g.rows.append(row)
        g.add(row)
    cap = MathTex(r"H_n(x)", r"\,e^{-x^2/2}", font_size=44, color=FG)
    cap[0][0:2].set_color(YELLOW)
    cap[1].set_color(PURPLE)
    cap.move_to([OSC_CX, 3.3, 0])
    g.caption = cap
    g.add(cap)
    return g


# ---------------------------------------------------------------- the notes' box (p63)
def notes_inset():
    """The notes' box, verbatim, top of the work area. Parts .h3 (8x^3), .m12 (- 12), .h4."""
    l1 = T("The first few Hermite polynomials are", size=30)
    l2 = MathTex(r"H_0 = 1,\quad H_1 = 2x,\quad H_2 = 4x^2 - 2,", font_size=36, color=FG)
    l3 = MathTex(r"H_3 = ", r"8x^3", r"- 12", r",\quad H_4 = ", r"16x^4 - 48x^2 + 12", r",\ \dots",
                 font_size=36, color=FG)
    body = VGroup(l1, l2, l3).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    border = RoundedRectangle(corner_radius=0.15, width=8.6, height=body.height + 0.5)
    border.set_stroke(FG, 2).set_fill(BG, 1).set_z_index(-1)
    border.move_to([2.2, 2.62, 0])
    body.move_to(border)
    g = VGroup(border, l1, l2, l3)
    g.border, g.l3 = border, l3
    g.h3, g.m12, g.h4 = l3[1], l3[2], l3[4]
    return g


class Ch5S6Ladder(NarratedScene):
    def construct(self):
        shot = load_scene("ch5_s5_assemble").handover_shot()
        self.add(shot)
        self.dl, self.ladder, self.rec = shot[0], shot[1], shot[2]
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ helpers
    def fill_rung(self, j, value, extra_fade=()):
        """value (already on screen at its rung place) becomes part of rung j."""
        r = self.ladder.rungs[j]
        self.play(r.label.animate.set_opacity(1), r.eq.animate.set_opacity(1),
                  *disappear(r.slot, *extra_fade), run_time=0.6)
        r.remove(r.slot)
        r.slot = None
        self.remove(value)
        r.value = value
        r.add(value)
        settle(self, self.ladder)

    def rung_tag(self, j, text, color):
        t = T(text, size=28, color=color)
        t.move_to([TAG_X + t.width / 2, self.ladder.rungs[j].label.get_center()[1], 0])
        return t

    # ------------------------------------------------------------ clip 1: H_3
    def clip1(self):
        lad, rec = self.ladder, self.rec
        with self.say("c5.ladder.1") as c:
            # {climb}: def line out, recursion to the top, ladder to the left
            c0 = _s2().LADDER_CENTER
            self.play(*during(disappear(self.dl), 0, 0.4),
                      *during(rec.animate.move_to(BOX_TOP), 0.15, 0.6),
                      *during(lad.animate.scale(L_SCALE, about_point=c0).shift(L_CENTER - c0), 0.45, 1.0),
                      run_time=min(2.6, 0.85 * c.until("Pause the video")))
            c.wait_until("Pause the video")
            # try H_3 yourself: the empty rung asks
            r3 = lad.rungs[3]
            q = MathTex("?", font_size=44, color=YELLOW)
            q.move_to([r3.slot.get_center()[0], r3.label.get_center()[1], 0])
            self.play(*appear(q), FlashAround(VGroup(r3.label, r3.slot), color=YELLOW, time_width=1.5),
                      run_time=1.6)
            self.q = q
            c.wait_until("three")
            # {three}: n = 2
            n2 = MathTex("n = 2", font_size=36, color=FG)
            n2[0][-1].set_color(GOLD)
            n2.move_to(rec[2])
            self.play(*swap(rec[2], n2), run_time=min(1.2, c.until("H three is")))
            self.n2 = n2
            c.wait_until("H three is")
            row_a = _at_eq(mrow(["H_3", "=", "2x", r"\cdot", "H_2", "-", "4", r"\cdot", "H_1"], size=48),
                           1, 1.55)
            self.play(FlashAround(rec[1], color=YELLOW, time_width=1.5),
                      *appear(row_a, shift=0.3 * DOWN), run_time=min(1.6, 0.8 * c.until("expand")))
            self.row_a = row_a
            c.wait_until("expand")
            # {expand}: 2x·H_2, H_2 copied from its rung
            row_b = _at_eq(mrow(["2x", r"\cdot", "H_2", "=", "2x", "(", "4x^2 - 2", ")", "=", "8x^3 - 4x"]),
                           3, 0.35)
            self.play(*fly(lad.rungs[2].value, row_b[6], arc=PI / 3), run_time=1.6)
            self.play(*appear(*[row_b[i] for i in range(6)], row_b[7], lag=0.05), run_time=0.9)
            c.wait_until("eight ex cubed")
            self.play(*appear(row_b[8], row_b[9], lag=0.15), run_time=1.0)
            settle(self, row_b)
            c.wait_until("Four times H one")
            # 4·H_1, H_1 copied from its rung
            row_c = _at_eq(mrow(["4", r"\cdot", "H_1", "=", "4", r"\cdot", "2x", "=", "8x"]), 3, -0.85)
            self.play(*fly(lad.rungs[1].value[0], row_c[6], arc=PI / 3), run_time=1.4)
            self.play(*appear(*[row_c[i] for i in range(6)], lag=0.05), run_time=0.8)
            c.wait_until("is eight ex", nth=1)
            self.play(*appear(row_c[7], row_c[8], lag=0.15), run_time=0.9)
            settle(self, row_c)
            c.wait_until("hthree")
            # {hthree}: take it away; H_3 fills the next rung
            row_d = _at_eq(mrow(["H_3", "=", "8x^3 - 12x"], size=48), 1, -2.2)
            self.play(*appear(row_d), FlashAround(row_c[8], color=YELLOW), run_time=1.1)
            c.wait_until("eight ex cubed", nth=1)
            v3 = _place(_s2().rung_value(3))
            self.play(*disappear(self.q),
                      *during(fly(row_d[2], v3), 0.2, 1.0), run_time=1.3)
            self.fill_rung(3, v3)
            self.rows1 = [row_b, row_c, row_d]

    # ------------------------------------------------------------ clip 2: the typo, parity
    def clip2(self):
        lad, row_a = self.ladder, self.row_a
        with self.say("c5.ladder.2") as c:
            # {typo}: the work rows go, H_3's line moves down, the notes' box comes in at the top
            ins = notes_inset()
            sweep_clear(self, row_a.animate.shift(np.array([0.9, 0.5 - 1.55, 0])), keep=[lad, row_a],
                        run_time=1.4)
            self.play(*appear(ins, shift=None), run_time=1.0)  # early: the notes' box, read whole
            c.wait_until("minus twelve")
            red = SurroundingRectangle(VGroup(ins.h3, ins.m12), color=RED, buff=0.06, corner_radius=0.08)
            red.set_stroke(width=3)
            self.play(FadeIn(red), run_time=0.8)
            c.wait_until("The lecturer corrected it")
            hx = T("x", size=44, color=YELLOW, slant=ITALIC).rotate(-0.15)
            hx.next_to(red, RIGHT, buff=0.02).shift(0.3 * UP)
            self.play(*appear(hx, shift=0.15 * DOWN), run_time=0.9)
            c.wait_until("parity")
            # {parity}: tags on the filled rungs
            self.play(FlashAround(VGroup(*[lad.rungs[j].value for j in range(3)]), color=YELLOW,
                                  time_width=1.5), run_time=1.5)
            c.wait_until("even powers")
            ev0, ev2 = self.rung_tag(0, "even powers only", EVEN_C), self.rung_tag(2, "even powers only", EVEN_C)
            self.play(*appear(ev0, ev2, lag=0.3), run_time=1.1)
            c.wait_until("only odd ones")
            od1 = self.rung_tag(1, "odd powers only", ODD_C)
            self.play(*appear(od1), run_time=0.9)
            c.wait_until("odd")
            # {odd}: both terms of H_3 are odd
            t1 = VGroup(row_a[2], row_a[3], row_a[4])
            self.play(FlashUnder(t1, color=ODD_C), *recolor([row_a[2], row_a[4]], ODD_C), run_time=1.2)
            c.wait_until("and H one")
            self.play(FlashUnder(row_a[8], color=ODD_C), *recolor([row_a[8]], ODD_C), run_time=1.0)
            c.wait_until("only odd powers")
            o1 = T("odd", size=30, color=ODD_C).next_to(t1, DOWN, buff=0.22)
            o2 = T("odd", size=30, color=ODD_C).next_to(row_a[8], DOWN, buff=0.22).set_y(o1.get_y())
            self.play(*appear(o1, o2, lag=0.3), run_time=1.0)
            c.wait_until("H three must too")
            od3 = self.rung_tag(3, "odd powers only", ODD_C)
            self.play(*appear(od3), run_time=1.0)
            c.wait_until("A lone twelve")
            cross = Cross(ins.m12, stroke_color=RED, stroke_width=6, scale_factor=1.15)
            self.play(Create(cross), run_time=0.9)
            self.ins, self.red, self.hx, self.cross = ins, red, hx, cross

    # ------------------------------------------------------------ clip 3: H_4
    def clip3(self):
        lad = self.ladder
        with self.say("c5.ladder.3") as c:
            # {four}: clear the H_3 work, keep the notes' box
            r4 = lad.rungs[4]
            self.play(FlashAround(VGroup(r4.label, r4.slot), color=YELLOW, time_width=1.5), run_time=1.2)
            sweep_clear(self, keep=[lad, self.ins, self.red, self.hx, self.cross],
                        run_time=min(1.2, c.until("H four is")))
            c.wait_until("H four is")
            ya, yb, yc, yd = 0.1, -1.0, -2.05, -3.15
            row_a = _at_eq(mrow(["H_4", "=", "2x", r"\cdot", "H_3", "-", "6", r"\cdot", "H_2"], size=48), 1, ya)
            n3 = MathTex("n = 3", font_size=36, color=FG)
            n3[0][-1].set_color(GOLD)
            n3.next_to(row_a, RIGHT, buff=0.6)
            self.play(*appear(row_a, n3, lag=0.3), run_time=1.0)
            row_b = _at_eq(mrow(["2x", r"\cdot", "H_3", "=", "2x", "(", "8x^3 - 12x", ")", "=",
                                 "16x^4 - 24x^2"]), 3, yb)
            row_c = _at_eq(mrow(["6", r"\cdot", "H_2", "=", "6", "(", "4x^2 - 2", ")", "=", "24x^2 - 12"]), 3, yc)
            self.play(*fly(lad.rungs[3].value, row_b[6], arc=PI / 4), run_time=1.2)
            c.wait_until("minus six")
            self.play(*fly(lad.rungs[2].value, row_c[6], arc=PI / 4), run_time=1.2)
            self.play(*appear(*[row_b[i] for i in range(6)], row_b[7],
                              *[row_c[i] for i in range(6)], row_c[7], lag=0.03), run_time=0.9)
            self.play(*appear(row_b[8], row_b[9], row_c[8], row_c[9], lag=0.15), run_time=1.0)
            settle(self, row_b)
            settle(self, row_c)
            c.wait_until("hfour")
            # {hfour}: subtract
            row_d = _at_eq(mrow(["H_4", "=", "16x^4 - 48x^2 + 12"], size=48), 1, yd)
            self.play(*appear(row_d), run_time=1.1)
            c.wait_until("notypo")
            v4 = _place(_s2().rung_value(4))
            self.play(*during(disappear(row_b, row_c), 0, 0.3), *during(fly(row_d[2], v4), 0.3, 1.0),
                      run_time=1.9)
            self.fill_rung(4, v4)
            # {notypo}: the notes' H_4 is right
            tick = check_mark(GREEN)
            cap = T("This is not the typo", size=30, color=GREEN)
            note = VGroup(tick, cap).arrange(RIGHT, buff=0.25)
            note.next_to(self.ins.border, DOWN, buff=0.25).set_x(self.ins.h4.get_x())
            self.play(FlashAround(self.ins.h4, color=GREEN), *appear(tick), run_time=1.2)
            c.wait_until("lecturer checked")
            self.play(*appear(cap), run_time=1.0)  # early: the lecturer's words, read as the voice says them

    # ------------------------------------------------------------ clip 4: why physicists care
    def clip4(self):
        lad = self.ladder
        with self.say("c5.ladder.4", gap=4.0) as c:
            # {why}: board clears, the ladder slides left
            k = L2_SCALE / L_SCALE
            c.wait_until("care")
            sweep_clear(self, lad.animate.scale(k, about_point=L_CENTER).shift(L2_CENTER - L_CENTER),
                        keep=[lad], run_time=min(2.0, c.until("osc")))
            c.wait_until("osc")
            plots = osc_plots()
            self.play(*appear(plots.caption), run_time=1.0)
            c.wait_until("wave functions")
            self.play(*appear(*plots.rows, lag=0.35, shift=None), run_time=2.2)  # early: labels n = 0..3 with their plots
            c.wait_until("zeros")
            self.play(VShowPassingFlash(plots.rows[0].curve.copy().set_stroke(YELLOW, 7), time_width=0.6),
                      run_time=1.4)
            c.wait_until("crosses zero")
            dots = [d for r in plots.rows for d in r.dots]
            self.play(*appear(*dots, lag=0.25, shift=None), run_time=2.0)
            c.wait_until("packet")
            pk = T("“localized packets of the wave function”", size=32, slant=ITALIC)
            pk.move_to([OSC_CX, -3.4, 0])
            self.play(*appear(pk), run_time=1.0)
