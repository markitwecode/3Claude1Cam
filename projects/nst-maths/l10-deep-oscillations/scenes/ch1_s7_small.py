"""Chapter 1, scene 7: small swings (arc vs reach, the sweep table, sin θ ≈ θ, ω = √(g/L), the big-swing flag). Clips c1.small.1 – c1.small.4.

Shared helpers (load_scene("ch1_s7_small")), for s8's recap:
  reach_line(theta)       the FG dashed reach, from the dashed vertical across to the bob.
  arc_line(theta)         s6's BLUE arc s at any angle (an empty VMobject near 0°).
  live_picture(tracker)   [pendulum, arc, reach] as always_redraw mobjects following tracker (θ in °):
                          add them, then play tracker.animate.set_value(60) for the {m3} sweep.
  readout(theta)          "θ = 30° = 0.52 rad" under the pendulum (YELLOW).
  small_rule()            θ̈ ≈ −(g/L) θ;  omega_boxed()  the YELLOW boxed ω = √(g/L) (.line .box).
"""
# style: 2
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
s3 = load_scene("ch1_s3_spring")
s5 = load_scene("ch1_s5_gravity")
s6 = load_scene("ch1_s6_arc")

OMEGA = 3.1321                      # √9.81, the 1 m pendulum (rad/s)
E_W2 = (r"\omega^2", FG, "pendulum g/L")   # "pendulum: g/L" is too wide: the legend would fall back to one column
READ_POS = np.array([s5.PIVOT[0], -1.05, 0])


# ── shared pieces ────────────────────────────────────────────────────────────────
def reach_line(theta=30):
    B = s5.bob_center(theta)
    A = np.array([s5.PIVOT[0], B[1], 0])
    if np.linalg.norm(B - A) < 0.06:
        return VMobject()
    return DashedLine(A, B, dash_length=0.12).set_stroke(FG, 4).set_z_index(2)


def arc_line(theta=30):
    if abs(theta) < 0.4:
        return VMobject()
    return s6.arc_s(theta)


def readout(theta=30):
    lab = MathTex(r"\theta =", font_size=34, color=YELLOW)
    d, r = round(theta), theta * DEGREES
    num = T(f"{d:.0f}° = {r:.2f} rad".replace("-", "−"), size=30, color=YELLOW)
    num.next_to(lab, RIGHT, buff=0.18).align_to(lab[0][0], DOWN)
    g = VGroup(lab, num)
    ref = VGroup(lab.copy(), T("30° = 0.52 rad", size=30).next_to(lab, RIGHT, buff=0.18))
    g.shift(READ_POS - ref.get_center())
    return g


def live_picture(tracker, with_readout=False):
    out = [always_redraw(lambda: s5.pendulum(tracker.get_value())),
           always_redraw(lambda: arc_line(tracker.get_value())),
           always_redraw(lambda: reach_line(tracker.get_value()))]
    if with_readout:
        out.append(always_redraw(lambda: readout(tracker.get_value())))
    return out


def small_rule():
    m = MathTex(r"\ddot{\theta}", r"\approx", "-", r"\frac{g}{L}", r"\,\theta", font_size=kit.COL_SIZE)
    m[0].set_color(RED)
    m[4].set_color(YELLOW)
    return m


def omega_boxed():
    line = MathTex(r"\omega", "=", r"\sqrt{g/L}", font_size=kit.COL_SIZE)
    box = SurroundingRectangle(line, color=YELLOW, buff=0.16).set_stroke(YELLOW, 3)
    g = VGroup(line, box)
    g.line, g.box = line, box
    return g


def math_theta_text(line):
    """CMU Serif's text θ reads as a script ϑ: swap each θ glyph of a kit text for TeX's."""
    chars = [ch for ch in getattr(line, "_src", "") if not ch.isspace()]
    if len(chars) != len(line.submobjects):
        return line
    for i, ch in enumerate(chars):
        if ch == "θ":
            g = line.submobjects[i]
            m = MathTex(r"\theta", color=g.get_color()).scale_to_fit_height(g.height * 0.98)
            m.move_to(g)
            line.submobjects[i] = m
    return line


def math_theta(card):
    for line in card.body:
        math_theta_text(line)
    return card


# ── scene helpers ────────────────────────────────────────────────────────────────
def at_left(mob, x, y):
    return mob.move_to([x, y, 0], aligned_edge=LEFT)


def step_at(text, y):
    return kit.step_label(text, (kit.COL_TOP - y) / kit.COL_PITCH + 0.5)


def ghost_arrow(a, b, color=RED):
    d = (b - a) / np.linalg.norm(b - a)
    n = np.array([-d[1], d[0], 0])
    tip_l, tip_w = 0.24, 0.11
    base = b - tip_l * d
    shaft = DashedLine(a, base, dash_length=0.12).set_stroke(color, 5)
    tip = Polygon(b, base + tip_w * n, base - tip_w * n).set_stroke(color, 1).set_fill(color, 1)
    return VGroup(shaft, tip).set_opacity(0.75).set_z_index(1)


def solid_arrow(a, b, color=RED):
    return Arrow(a, b, buff=0, stroke_width=5, tip_length=0.24,
                 max_tip_length_to_length_ratio=0.45, color=color).set_z_index(1)


# table layout (right column, under the boxed rule)
X_TH, X_SIN, X_PCT = 0.95, 4.0, 6.5
Y_HEAD = 0.3
Y_ROWS = [-0.35, -0.95, -1.55, -2.15]
RULE_Y = 1.2                        # the boxed rule steps down 0.3 under the move card
ROWS = [("0.1", "0.0998", r"0.2\%"),
        (r"10^\circ = 0.1745", "0.1736", r"0.5\%"),
        (r"30^\circ = 0.5236", "0.5000", r"4.5\%"),
        (r"60^\circ = 1.047", "0.866", r"17\%")]
ROW_DEG = [0.1 / DEGREES, 10, 30, 60]


def table_cell(tex, col, y, color=FG, size=34):
    m = MathTex(tex, font_size=size, color=color)
    if col == 2:
        return m.move_to([X_PCT, y, 0], aligned_edge=RIGHT)
    return at_left(m, X_TH if col == 0 else X_SIN, y)


class SmallSwings(NarratedScene):
    def construct(self):
        H = s6.handover_shot()
        self.add(H)
        self.remove(H)
        self.add(H.pend, H.arc, H.s_label, H.rule, H.legend, H.tag)
        self.pend, self.arc, self.slab, self.R, self.leg, self.ctag = (
            H.pend, H.arc, H.s_label, H.rule, H.legend, H.tag)
        self.th = ValueTracker(30)
        self.live = []
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── live / static picture ──
    def go_live(self, statics, readout_on):
        self.remove(*[m for s in statics for m in s.get_family()])
        self.live = live_picture(self.th, readout_on)
        self.add(*self.live)

    def freeze(self, readout_on):
        v = self.th.get_value()
        self.remove(*self.live)
        self.live = []
        pics = [s5.pendulum(v), arc_line(v), reach_line(v)]
        if readout_on:
            pics.append(readout(v))
        self.add(*pics)
        return pics

    # ── c1.small.1: the move; reach L sin θ vs arc L θ ──
    def clip1(self):
        pend, arc = self.pend, self.arc
        card = math_theta(kit.move_card("For small swings, trade sin θ for θ: arc and reach almost agree."))
        reach = reach_line(30)
        B = pend.B
        lab_reach = MathTex(r"L", r"\sin", r"\theta", font_size=30)
        lab_reach[2].set_color(YELLOW)
        lab_reach.move_to([(s5.PIVOT[0] + B[0]) / 2 + 0.12, B[1] + 0.26, 0])
        a = -PI / 2 - 15 * DEGREES
        lab_arc = MathTex(r"s", "=", r"L", r"\theta", font_size=32, color=BLUE)
        lab_arc.move_to(s5.PIVOT + (s5.ROD_L + 0.55) * np.array([np.cos(a), np.sin(a), 0]) + 0.35 * LEFT)
        self.card, self.reach, self.lab_reach, self.lab_arc = card, reach, lab_reach, lab_arc

        with self.say("c1.small.1") as c:
            self.play(*appear(card, shift=None), self.R.animate.shift((RULE_Y - self.R.get_y()) * UP),  # early: the move card states the scene's move as it is named
                      run_time=1.2)
            c.wait_until("reach")
            self.play(VShowPassingFlash(arc.copy().set_stroke(YELLOW, 9), time_width=0.8), run_time=1.4)
            c.wait_until("sideways reach")
            self.play(*during(disappear(self.slab), 0, 0.4), *during([Create(reach)], 0.3, 1), run_time=1.6)
            c.wait_until("L times sine")
            self.play(*appear(lab_reach, shift=None), run_time=1.0)
            c.wait_until("the side opposite")
            self.play(FlashAround(pend.theta_label, time_width=1.5),
                      VShowPassingFlash(reach.copy().set_stroke(YELLOW, 7), time_width=0.8), run_time=1.4)
            c.wait_until("arc_len")
            self.play(*appear(lab_arc, shift=None),
                      VShowPassingFlash(arc.copy().set_stroke(YELLOW, 9), time_width=0.8), run_time=1.4)
            c.wait_until("almost agree")
            self.play(*flash([lab_reach, lab_arc]), run_time=min(1.5, c.until(floor=0.8)))

    # ── c1.small.2: the sweep and the growing table ──
    def clip2(self):
        th = self.th
        head = VGroup(table_cell(r"\theta\ (\text{rad})", 0, Y_HEAD, YELLOW, 30),
                      table_cell(r"\sin\theta", 1, Y_HEAD, FG, 30),
                      table_cell(r"\text{short by}", 2, Y_HEAD, GOLD, 30))
        rule_ln = Line([X_TH, Y_HEAD - 0.32, 0], [X_PCT, Y_HEAD - 0.32, 0]).set_stroke(DIM, 1.5)
        rows = [[table_cell(r[0], 0, y, YELLOW), table_cell(r[1], 1, y), table_cell(r[2], 2, y, GOLD)]
                for r, y in zip(ROWS, Y_ROWS)]
        rd = readout(30)
        self.table = VGroup(head, rule_ln, *[m for r in rows for m in r])

        def step(k, cue_next, rt):
            self.play(th.animate.set_value(ROW_DEG[k]),
                      *appear(rows[k][0], rows[k][1], lag=0.5, shift=None),
                      run_time=min(rt, 0.8 * c.until(cue_next)))

        with self.say("c1.small.2") as c:
            self.play(*during(disappear(self.lab_reach, self.lab_arc), 0, 0.45),  # early: the table's header is shown whole, then filled row by row
                      *during(appear(head, rule_ln, rd, lag=0.2, shift=None), 0.45, 1), run_time=1.6)
            self.go_live([self.pend, self.arc, self.reach, rd], True)
            self.play(th.animate.set_value(0), run_time=min(2.2, c.until("r1")))
            c.wait_until("r1")
            self.play(th.animate.set_value(ROW_DEG[0]), *appear(rows[0][0], shift=None),
                      run_time=min(1.8, c.until("the sine is")))
            c.wait_until("the sine is")
            self.play(*appear(rows[0][1], shift=None), run_time=1.0)
            c.wait_until("two tenths")
            self.play(*appear(rows[0][2], shift=None), run_time=1.0)
            c.wait_until("r2")
            step(1, "half a percent", 1.8)
            c.wait_until("half a percent")
            self.play(*appear(rows[1][2], shift=None), run_time=1.0)
            c.wait_until("r3")
            step(2, "four and a half", 2.2)
            c.wait_until("four and a half")
            self.play(*appear(rows[2][2], shift=None), run_time=1.0)
            c.wait_until("r4")
            step(3, "seventeen", 3.2)
            c.wait_until("seventeen")
            self.play(*appear(rows[3][2], shift=None), run_time=1.0)
            c.wait_until("starts to fail")
            self.play(*recolor([rows[3][2]], RED), FlashAround(rows[3][2], color=RED, time_width=1.5),
                      run_time=min(1.4, c.until(floor=0.8)))

    # ── c1.small.3: trade sin θ for θ; match the spring; ω = √(g/L); the 1 m numbers ──
    def clip3(self):
        th, R = self.th, self.R
        L1 = MathTex(r"\sin", r"\theta", r"\approx", r"\theta", font_size=kit.COL_SIZE)
        L1[1].set_color(YELLOW)
        L1[3].set_color(YELLOW)
        L1.move_to([4.25, R.get_center()[1], 0], aligned_edge=LEFT)
        t1 = kit.tag("small swings", L1, DOWN, buff=0.18).align_to(L1, LEFT)
        L2 = at_left(small_rule(), kit.COL_LEFT, -0.05)
        st2 = step_at("trade sin θ for θ", 0.5)
        math_theta_text(st2[1])
        spring = s3.rule_boxed()
        spring.move_to([4.25, L2.get_center()[1], 0], aligned_edge=LEFT)
        L3 = MathTex(r"\omega^2", "=", r"\frac{g}{L}", font_size=kit.COL_SIZE)
        at_left(L3, kit.COL_LEFT, -1.15)
        st3 = step_at("match the two", -0.6)
        W = omega_boxed()
        at_left(W, kit.COL_LEFT, -2.3)
        st4 = step_at("square root", -1.72)
        t108 = kit.tag("notes p. 108: stated there, built here", W, DOWN, buff=0.16).align_to(W, LEFT)
        N1 = MathTex(r"L = 1\text{ m}:", r"\quad \omega^2 = 9.81", font_size=kit.COL_SIZE)
        N1[0].set_color(DIM)
        N1.move_to([3.05, L3.get_center()[1], 0], aligned_edge=LEFT)
        N2 = MathTex(r"\omega \approx 3.13\ \text{per second}", font_size=kit.COL_SIZE)
        N2.move_to([W.get_right()[0] + 0.45, W.get_center()[1], 0], aligned_edge=LEFT)
        self.L1, self.t1, self.L2, self.st2, self.spring = L1, t1, L2, st2, spring
        self.L3, self.st3, self.W, self.st4, self.t108, self.N1, self.N2 = L3, st3, W, st4, t108, N1, N2

        with self.say("c1.small.3") as c:
            self.play(th.animate.set_value(10),
                      *during(appear(L1, t1, lag=0.3, shift=None), 0.4, 1), run_time=2.0)
            c.wait_until("theta double dot")
            self.play(*disappear(self.table), run_time=0.8)
            derive(self, R.line, L2, run_time=min(2.0, 0.8 * c.until("match")))
            self.play(*appear(st2, shift=None), *set_alpha([R], 0.4), run_time=0.8)
            c.wait_until("match")
            spring.save_state()
            spring.shift(RIGHT * 2.5).set_opacity(0)
            self.play(spring.animate.restore(), run_time=1.4)
            c.wait_until("exactly")
            self.play(*flash([VGroup(*L2[2:4]), spring.line[2]]), run_time=1.3)
            c.wait_until("omega squared")
            leg_new = [E_W2 if e[0] == r"\dot{x}" else e for e in self.leg.entries]   # ω² takes ẋ's row
            kit.legend_set(self, self.leg, leg_new, *appear(st3, L3, lag=0.3, shift=None), *set_alpha([L1, t1], 0.4), run_time=min(1.6, c.until("root")))  # early: the legend entry is the match being said
            c.wait_until("root")
            self.play(*appear(st4, W.line, lag=0.3, shift=None), run_time=1.2)
            self.play(FadeIn(W.box), *appear(t108, shift=None), run_time=1.0)
            settle(self, W, add=[W.line, W.box])
            c.wait_until("a longer pendulum")
            self.play(FlashAround(W.line[2], time_width=1.5),
                      VShowPassingFlash(Line(s5.PIVOT, s5.bob_center(10)).set_stroke(YELLOW, 8), time_width=0.8),
                      run_time=1.4)
            c.wait_until("for each radian")
            self.play(FlashAround(L2[4], time_width=1.5), run_time=1.3)
            c.wait_until("numbers")
            self.play(*appear(N1, shift=None), *set_alpha([spring, st2], 0.4), run_time=1.2)
            c.wait_until("so omega is about")
            self.play(*appear(N2, shift=None), run_time=1.2)
            # the pendulum swings gently at 10°, at its own rate (period 2π/ω ≈ 2.0 s)
            period = TAU / OMEGA
            n = int(max(1.0, (c.until() - 0.15) // period))
            self.play(UpdateFromAlphaFunc(th, lambda m, a: m.set_value(10 * np.cos(TAU * n * a))),
                      run_time=n * period, rate_func=linear)
            th.set_value(10)

    # ── c1.small.4: the honest warning at 60°; the corner tag leaves ──
    def clip4(self):
        th = self.th
        col = [self.R, self.L1, self.t1, self.st2, self.spring, self.st3, self.L3, self.N1,
               self.st4, self.W, self.t108, self.N2]
        u, t = s5._dirs(60)
        B = s5.bob_center(60)
        G = 1.8
        S0 = B + 0.3 * t
        true = solid_arrow(S0, S0 + G * np.sin(PI / 3) * t)
        g0 = S0 + 0.34 * u
        ghost = ghost_arrow(g0, g0 + G * (PI / 3) * t)
        lab_true = MathTex(r"mg\sin\theta", font_size=30, color=RED)
        lab_true.move_to(S0 + 0.8 * t - 0.78 * u)
        lab_ghost = MathTex(r"\text{the rule's pull, }mg\,\theta", font_size=30, color=RED)
        lab_ghost.set_opacity(0.85).move_to([-4.75, ghost[1].get_bottom()[1] - 0.3, 0])
        ftag = VGroup(kit.tag("big swings:"), kit.tag("a weaker pull than"),
                      kit.tag("the rule says (part two)")).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        ftag.move_to([-2.75, 0.35, 0], aligned_edge=LEFT)

        with self.say("c1.small.4") as c:
            pend_st, arc_st, reach_st, rd_st = self.freeze(True)
            self.remove(pend_st)
            self.live = [always_redraw(lambda: s5.pendulum(th.get_value()))]
            self.add(*self.live)
            self.play(*during(disappear(arc_st, reach_st, rd_st), 0, 0.4), th.animate.set_value(60),
                      *set_alpha(col, DIMMED), run_time=min(2.2, c.until("big angles")))
            self.remove(*self.live)
            pend60 = s5.pendulum(60)
            self.add(pend60)
            c.wait_until("really pulls")
            self.play(GrowArrow(true), *appear(lab_true, shift=None), run_time=1.4)
            c.wait_until("which uses theta")
            self.play(Create(ghost), *appear(lab_ghost, shift=None), run_time=1.5)
            c.wait_until("big swings")
            self.play(*appear(ftag, lag=0.3, shift=None), run_time=1.2)
            c.wait_until("approximation")
            self.play(FlashAround(self.L2[1], time_width=1.5), run_time=1.3)
            c.wait_until("done")
            self.remove(pend60)
            self.live = [always_redraw(lambda: s5.pendulum(th.get_value()))]
            self.add(*self.live)
            self.play(*during(disappear(self.ctag, true, ghost, lab_true, lab_ghost), 0, 0.45),
                      *during([th.animate.set_value(10)], 0.2, 1),
                      *set_alpha([self.W], 1), run_time=1.6)
            self.play(FlashAround(self.W, time_width=1.5), run_time=min(1.3, c.until(floor=0.8)))
            self.remove(*self.live)
            self.add(s5.pendulum(10))
