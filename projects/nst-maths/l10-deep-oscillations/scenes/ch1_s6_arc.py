"""Chapter 1, scene 6: from angle to distance (Newton along the swing, s = Lθ, the pendulum's rule). Clips c1.arc.1 – c1.arc.4.

Shared helpers (load_scene("ch1_s6_arc")):
  arc_s()          the BLUE arc s from the bottom of the swing up to the bob at 30°.
  s_label()        the BLUE "s" inside that arc.
  pend_rule_boxed()  the boxed θ̈ = −(g/L) sin θ (.line .box), built at ORIGIN.
  E_S              legend entry for s; HANDOVER_ENTRIES = s5's FINAL_ENTRIES + E_S (max_rows 4).
  handover_shot()  this scene's last frame (s7 opens on it): .pend .arc .s_label .rule .legend .tag
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

kit = load_scene("ch1_s2_tools")
s5 = load_scene("ch1_s5_gravity")
s3 = load_scene("ch1_s3_spring")

E_S = ("s", BLUE, "arc distance")
HANDOVER_ENTRIES = list(s5.FINAL_ENTRIES) + [E_S]
COL_W = kit.COL_RIGHT - kit.COL_LEFT - 0.05


# ── shared pieces ────────────────────────────────────────────────────────────────
def arc_s(theta=30):
    return Arc(radius=s5.ROD_L, start_angle=-PI / 2, angle=-theta * DEGREES,
               arc_center=s5.PIVOT).set_stroke(BLUE, 6).set_z_index(2)


def s_label(theta=30):
    a = -PI / 2 - theta * DEGREES / 2
    return MathTex("s", font_size=36, color=BLUE).move_to(
        s5.PIVOT + (s5.ROD_L - 0.4) * np.array([np.cos(a), np.sin(a), 0]))


def pend_rule_line():
    m = MathTex(r"\ddot{\theta}", "=", "-", r"\frac{g}{L}", r"\sin", r"\theta", font_size=kit.COL_SIZE)
    m[0].set_color(RED)
    m[5].set_color(YELLOW)
    return m


def pend_rule_boxed():
    line = pend_rule_line()
    box = SurroundingRectangle(line, color=YELLOW, buff=0.16).set_stroke(YELLOW, 3)
    g = VGroup(line, box)
    g.line, g.box = line, box
    return g


def handover_shot():
    """Last frame of s6 = first of s7: pendulum at 30° with the BLUE arc s, the boxed
    θ̈ = −(g/L) sin θ at the top of the column, the 8-entry legend and the corner tag."""
    pend = s5.pendulum(30)
    arc = arc_s()
    lab = s_label()
    rule = pend_rule_boxed().move_to(kit.col_point(0), aligned_edge=LEFT)
    leg = kit.legend(HANDOVER_ENTRIES, s5.LEG_ROWS)
    tag_ = kit.corner_tag()
    g = VGroup(pend, arc, lab, rule, leg, tag_)
    g.pend, g.arc, g.s_label, g.rule, g.legend, g.tag = pend, arc, lab, rule, leg, tag_
    return g


# ── scene helpers ────────────────────────────────────────────────────────────────
def place(mob, y):
    if mob.width > COL_W:
        mob.scale_to_fit_width(COL_W)
    return mob.move_to([kit.COL_LEFT, y, 0], aligned_edge=LEFT)


def step_at(text, y):
    return kit.step_label(text, (kit.COL_TOP - y) / kit.COL_PITCH + 0.5)


def strike(m):
    return Line(m.get_corner(DL) + 0.04 * (DL), m.get_corner(UR) + 0.04 * UR).set_stroke(YELLOW, 4)


def pulse_ms(L1):
    """The two struck-out m's swell and glow YELLOW, then settle back (a colour pulse, no box)."""
    return [m.animate(rate_func=there_and_back).set_color(YELLOW).scale(1.3) for m in (L1[0], L1[5])]


WORDS_SWING = r"\left(\begin{matrix}\text{acceleration}\\ \text{along the swing}\end{matrix}\right)"


class ArcScene(NarratedScene):
    def construct(self):
        H = s5.handover_shot()
        self.add(H)
        pend, S, F, leg, ctag = H.pend, H.split, H.force, H.legend, H.tag
        self.pend, self.S, self.F, self.leg = pend, S, F, leg
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.handover()

    # ── c1.arc.1: Newton along the swing; the mass cancels ──
    def clip1(self):
        S, F = self.S, self.F
        L1 = MathTex("m", r"\times", WORDS_SWING, "=", "-", "m", "g", r"\sin", r"\theta",
                     font_size=kit.COL_SIZE)
        L1[8].set_color(YELLOW)
        place(L1, 0.4)
        st1 = step_at("Newton, along the swing", 0.98)
        L2 = MathTex(WORDS_SWING, "=", "-", "g", r"\sin", r"\theta", font_size=kit.COL_SIZE)
        L2[5].set_color(YELLOW)
        place(L2, -0.92)
        st2 = step_at("divide by m", -0.27)
        k1, k2 = strike(L1[0]), strike(L1[5])
        self.L1, self.L2, self.st1, self.st2, self.strikes = L1, L2, st1, st2, (k1, k2)

        with self.say("c1.arc.1") as c:
            self.play(VShowPassingFlash(S.swing.copy().set_stroke(YELLOW, 9), time_width=0.8),
                      run_time=1.4)
            c.wait_until("the mass times")
            self.play(*appear(st1, L1, lag=0.4, shift=None), run_time=min(1.8, c.until("equals minus")))
            c.wait_until("equals minus")
            self.play(FlashAround(VGroup(*L1[4:]), time_width=1.5), run_time=1.5)
            c.wait_until("divide")
            self.play(Create(k1), Create(k2), run_time=1.2)
            derive(self, L1, L2, *set_alpha([F], 0.4), run_time=2.0)
            self.play(*appear(st2, shift=None), run_time=0.8)
            c.wait_until("The mass is gone")
            self.play(*pulse_ms(L1), run_time=1.3)

    # ── c1.arc.2: the think stop; heavier bob, same swing; the spring contrast ──
    def clip2(self):
        pend, S, leg = self.pend, self.S, self.leg
        box = kit.think_box("Swap the bob for one twice as heavy.\nDoes the pendulum swing\n"
                            "faster, slower, or the same?", size=30)
        ring = kit.think_ring()
        ans = T("The same.", size=40, color=GREEN).move_to(box.box)

        big_bob = Circle(radius=0.42).set_fill(BLUE, 1).set_stroke(BLUE, 2).move_to(pend.B).set_z_index(3)
        lab2m = MathTex("2m", font_size=30, color=BG).move_to(pend.B).set_z_index(4)
        S2 = s5.gravity_split(30, label=False, G=2 * s5.G_LEN)
        lab2mg = MathTex("2mg", font_size=32).move_to(pend.B + np.array([0.62, -1.45, 0]))
        self.lab2m, self.lab2mg = lab2m, lab2mg

        # the comparison grid (right column, lower half)
        xs = [3.35, 4.6, 5.85]
        yh, y1, y2 = -1.75, -2.4, -3.05
        head = VGroup(*[T(w, size=26, color=DIM).move_to([x, yh, 0]) for w, x in zip(["pull", "mass", "swing"], xs)])

        def row(name, vals, y, last_col):
            nm = T(name, size=30).move_to([kit.COL_LEFT, y, 0], aligned_edge=LEFT)
            cells = [T(v, size=30, color=col).move_to([x, y, 0])
                     for v, x, col in zip(vals, xs, [FG, FG, last_col])]
            return VGroup(nm, *cells)

        r_pend = row("pendulum", ["×2", "×2", "same"], y1, GREEN)
        r_spr = row("spring", ["same", "×2", "slower"], y2, RED)
        mini = VGroup(s3.spring_drawing(2.0, zero=False), s3.pull_arrow(2.0))
        mini.scale_to_fit_width(1.9).move_to([-0.95, y2 + 0.1, 0])
        self.grid = VGroup(head, r_pend, r_spr, mini)

        with self.say("c1.arc.2") as c:
            self.play(*appear(box, shift=None), FadeIn(ring), run_time=1.2)  # early: the question is shown whole, then read
            self.play(kit.drain(ring, run_time=max(1.0, c.until("same") - 0.2)))
            c.wait_until("same")
            self.play(*swap(box, ans), *disappear(ring), run_time=1.2)
            c.wait_until("Twice the mass")
            self.play(*during(disappear(leg), 0, 0.4),
                      *during([Transform(pend.bob, big_bob)], 0.3, 1),
                      *during(swap(pend.m_label, lab2m), 0.3, 1), run_time=1.4)
            c.wait_until("twice the weight")
            self.play(Transform(S.weight, S2.weight), Transform(S.along, S2.along),
                      Transform(S.corner, S2.corner), *swap(S.weight_label, lab2mg), run_time=1.5)
            c.wait_until("so the pull doubles")
            self.play(Transform(S.swing, S2.swing), run_time=1.3)
            c.wait_until("and the two cancel")
            self.play(*pulse_ms(self.L1), run_time=1.3)
            c.wait_until("spring_contrast")
            self.play(*during(disappear(ans), 0, 0.4),  # early: the grid's header and the pendulum row sum up what was just said
                      *during(appear(head, r_pend, lag=0.3, shift=None), 0.4, 1), run_time=1.5)
            c.wait_until("its pull depends")
            self.play(*appear(mini, r_spr, lag=0.3, shift=None), run_time=1.4)  # early: the spring row is read across the sentence
            c.wait_until("was slower")
            self.play(FlashAround(r_spr[3], color=RED, time_width=1.5), run_time=min(1.3, c.until(floor=0.6)))

    # ── c1.arc.3: the snag; the arc turns angle into distance; differentiate twice ──
    def clip3(self):
        pend, S, leg, F = self.pend, self.S, self.leg, self.F
        L1, L2 = self.L1, self.L2
        small = s5.pendulum(30)
        S1 = s5.gravity_split(30)
        arc = arc_s()
        slab = s_label()
        card = kit.arc_card(small=True)
        card.scale(22 / 18).move_to([3.8, -1.45, 0])

        L3 = MathTex("s", "=", "L", r"\theta", font_size=kit.COL_SIZE)
        L3[0].set_color(BLUE)
        L3[3].set_color(YELLOW)
        place(L3, 0.85)
        t3 = kit.tag("arc = radius × angle", L3, RIGHT, buff=0.45)
        L4 = MathTex(r"\dot{s}", "=", "L", r"\dot{\theta}", font_size=kit.COL_SIZE)
        L4[0].set_color(GREEN)
        L4[3].set_color(GREEN)
        place(L4, 0.0)
        st4 = step_at("differentiate; L is fixed", 0.42)
        L5 = MathTex(r"\ddot{s}", "=", "L", r"\ddot{\theta}", font_size=kit.COL_SIZE)
        L5[0].set_color(RED)
        L5[3].set_color(RED)
        place(L5, -0.85)
        st5 = step_at("differentiate again", -0.43)
        self.L3, self.L4, self.L5, self.t3, self.st4, self.st5 = L3, L4, L5, t3, st4, st5
        self.arc, self.slab = arc, slab

        with self.say("c1.arc.3") as c:
            d = (2.3 - L2.get_center()[1]) * UP
            self.play(*during(disappear(self.grid, F, L1, self.st1, self.st2, *self.strikes), 0, 0.45),
                      *during([L2.animate.shift(d)], 0.35, 1), run_time=1.6)
            c.wait_until("Newton counts")
            self.play(Transform(pend.bob, small.bob), *swap(self.lab2m, small.m_label),  # early: the legend returns whole
                      Transform(S.weight, S1.weight), Transform(S.along, S1.along),
                      Transform(S.corner, S1.corner), Transform(S.swing, S1.swing),
                      *swap(self.lab2mg, S1.weight_label), *appear(leg, shift=None), run_time=1.6)
            self.mg_label = S1.weight_label
            c.wait_until("by its angle")
            self.play(FlashAround(pend.theta_label, time_width=1.5), run_time=1.3)
            c.wait_until("arc")
            self.play(Create(arc), *appear(card, shift=None), run_time=1.6)
            c.wait_until("circle of radius L")
            self.play(VShowPassingFlash(pend.rod.copy().set_stroke(YELLOW, 8), time_width=0.8),
                      FlashAround(pend.L_label, time_width=1.5), run_time=1.4)
            c.wait_until("its distance along the arc")
            kit.legend_add(self, leg, E_S, extra=appear(slab), run_time=1.2)
            c.wait_until("is L times theta")
            self.play(*appear(L3, t3, lag=0.4, shift=None), run_time=1.3)
            c.wait_until("in radians")
            self.play(FlashAround(L3[3], time_width=1.5), run_time=1.2)
            c.wait_until("twice")
            derive(self, L3, L4, *disappear(card), run_time=1.8)
            self.play(*appear(st4, shift=None), run_time=0.7)
            c.wait_until("the acceleration along the arc")
            self.play(*appear(st5, L5, lag=0.4, shift=None), run_time=1.6)
            br = Brace(L2[0], DOWN, buff=0.06, color=DIM)
            blab = MathTex(r"\ddot{s}", font_size=32, color=RED).next_to(br, DOWN, buff=0.08)
            self.brace, self.blab = br, blab
            self.play(GrowFromCenter(br), *appear(blab, shift=None), FlashAround(L5[0], time_width=1.5),
                      run_time=min(1.4, c.until(floor=0.8)))

    # ── c1.arc.4: substitute, divide by L, compare with the spring ──
    def clip4(self):
        L2, L3, L4, L5 = self.L2, self.L3, self.L4, self.L5
        L6 = MathTex("L", r"\ddot{\theta}", "=", "-", "g", r"\sin", r"\theta", font_size=kit.COL_SIZE)
        L6[1].set_color(RED)
        L6[6].set_color(YELLOW)
        place(L6, -1.7)
        st6 = step_at("substitute", -1.28)
        R = pend_rule_boxed()
        R.move_to([kit.COL_LEFT, -2.75, 0], aligned_edge=LEFT)
        st7 = step_at("divide by L", -2.15)
        spring = s3.rule_boxed()
        R_top = R.copy().move_to(kit.col_point(0), aligned_edge=LEFT)
        spring.move_to([R_top.get_right()[0] + 0.55 + spring.width / 2, R_top.get_center()[1], 0])
        spring_start = spring.copy().shift(RIGHT * 2.5)
        almost = T("almost", size=32, color=YELLOW).move_to(
            [(R_top.get_right()[0] + spring.get_left()[0]) / 2, R_top.get_top()[1] + 0.4, 0])
        hard = kit.tag("no answer in familiar functions", R_top, DOWN, buff=0.3)
        hard.align_to(R_top, LEFT)
        self.spring_rule, self.almost, self.hard, self.R = spring, almost, hard, R

        with self.say("c1.arc.4") as c:
            self.play(*flash([VGroup(*L5[2:]), VGroup(*L2[1:])]), run_time=1.4)
            c.wait_until("the length L times")
            self.play(*appear(st6, L6, lag=0.4, shift=None), *set_alpha([L3, L4, self.t3], 0.4),
                      run_time=min(1.6, c.until("divide_L")))
            c.wait_until("divide_L")
            self.play(*appear(st7, R.line, lag=0.5, shift=None),
                      *set_alpha([L2, self.brace, self.blab, L5, self.st4, self.st5], 0.4), run_time=1.8)
            c.wait_until("theta double dot equals", nth=1)
            self.play(FadeIn(R.box), *set_alpha([L6, st6], 0.4), run_time=1.0)
            settle(self, R, add=[R.line, R.box])
            c.wait_until("compare")
            old = [L2, self.brace, self.blab, L3, self.t3, L4, self.st4, L5, self.st5, L6, st6, st7]
            self.play(*during(disappear(*old), 0, 0.45),
                      *during([R.animate.move_to(kit.col_point(0), aligned_edge=LEFT)], 0.35, 1),
                      run_time=1.6)
            spring.save_state()
            spring.move_to(spring_start)
            spring.set_opacity(0)
            self.play(spring.animate.restore(), run_time=1.4)
            c.wait_until("almost")
            self.play(*appear(almost), *flash([VGroup(R.line[4], R.line[5]), spring.line[3]]),
                      run_time=1.5)
            c.wait_until("hard")
            self.play(*appear(hard), run_time=1.0)  # early: the tag captions the whole sentence

    # ── handover: keep the pendulum, the arc s, the boxed rule, legend, tag ──
    def handover(self):
        S = self.S
        S.remove(S.weight_label)
        self.wait(1.0)
        self.play(*disappear(S, self.mg_label, self.spring_rule, self.almost, self.hard), run_time=1.2)
        final = handover_shot()
        self.clear()
        self.add(final)
        self.wait(1.0)
