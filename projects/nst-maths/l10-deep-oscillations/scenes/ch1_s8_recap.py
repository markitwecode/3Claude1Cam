"""Chapter 1, scene 8: one rule for both machines, simple harmonic motion, the recap, next time. Clips c1.recap.1 – c1.recap.3.

Reused drawings (never redrawn): s3's spring (spring_drawing, pull_arrow, rule_boxed), s5's pendulum
(pendulum, gravity_split), s7's sweep (live_picture), kit's legend / move cards / tags, s1's _faded.
Reversed join: the last frame is exactly load_scene("ch2_s1_hook").opening_card() (chapter 2's first
frame); the {next} line and dot morph into its table and block during the end hold.
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
spr = load_scene("ch1_s3_spring")
grav = load_scene("ch1_s5_gravity")
s7 = load_scene("ch1_s7_small")
hook = load_scene("ch1_s1_hook")
ch2 = load_scene("ch2_s1_hook")

OM = 3.13                         # s1's beat (1 m pendulum), rad/s
SPRING_ORIGIN = np.array([spr.SPRING_REST_X, spr.SPRING_Y, 0])

# {both}: spring left, pendulum right, the rule between
B_SP_REST, B_SP_Y, B_SP_S, B_SP_AMP = -4.1, 0.2, 0.65, 3.0
B_PIV, B_PD_S, B_PD_AMP = np.array([4.5, 2.55, 0]), 0.8, 20.0
B_SPLIT_G = 3.0                   # longer mg, so the along-swing pull reads at 20°
RULE_AT = np.array([0.6, 2.0, 0])
SHM_AT = np.array([0.6, 0.85, 0])
OMEGA_Y = -0.75                   # the 5-row legend's top is at y ≈ -1.33: the spring can't go lower

# {recap}: three columns
REC_TOP, REC_PIV_Y, REC_PD_S = 3.3, 1.45, 0.75
REC_SP_S, REC_SP_Y = 0.58, 0.25
SHM_BAND_Y = -2.05                # the shrunk "simple harmonic motion" row, under the columns
FACTS_Y = -2.85

# {next}: the dot on its line, the turning arrow above
N_REST, N_LINE_Y, N_R = spr.SPRING_REST_X, -1.6, ch2.WAVE_AMP     # 1.3 = ch2's circle radius
N_CENTER = np.array([N_REST, 0.1, 0])
N_OM = ch2.OMEGA                  # 2 rad/s, ch2's beat
N_TEXT_X = 2.9

S3_MOVE = "Name the pull, then let Newton turn it into an acceleration."
S5_MOVE = "Split gravity along the rod and the swing: only the swing part drives."
S7_MOVE = "For small swings, trade sin θ for θ: arc and reach almost agree."
S7_LINES = ["For small swings,", "trade sin θ for θ:", "arc and reach almost agree."]   # keep "sin θ" together

E_X_ALL = (r"x", BLUE, "displacement (spring: distance · pendulum: angle)")
START_ENTRIES = [grav.E_X_SHORT, kit.E_XD, kit.E_XDD, grav.E_TH, spr.E_W]
FINAL_ENTRIES = [E_X_ALL, kit.E_XD, kit.E_XDD, spr.E_W]


def place_spring(m, rest, y, s):
    """s3's spring drawing (built at its own rest point) scaled by s, rest point moved to (rest, y)."""
    m.scale(s, about_point=SPRING_ORIGIN)
    m.shift(np.array([rest, y, 0]) - SPRING_ORIGIN)
    return m


def place_pendulum(m, pivot, s):
    """s5's pendulum (built at its own pivot) scaled by s about the pivot, pivot moved to `pivot`."""
    m.scale(s, about_point=grav.PIVOT)
    m.shift(np.array(pivot) - grav.PIVOT)
    return m


def swing_pull(theta, G=B_SPLIT_G):
    """s5's RED along-swing part of gravity, moved to start at the bob."""
    gs = grav.gravity_split(theta, label=False, G=G)
    return gs.swing.shift(gs.B - gs.C)


def omega_sq(num, den):
    m = MathTex(r"\omega^2", "=", r"\frac{" + num + "}{" + den + "}", font_size=42)
    return m


def facts_line():
    parts = [MathTex(r"F = m\ddot{x}", font_size=30),
             MathTex(r"\text{Hooke: } F = -kx", font_size=30),
             MathTex(r"g = 9.81\ \text{m/s}^2", font_size=30),
             MathTex(r"\text{arc} = \text{radius} \times \text{angle (radians)}", font_size=30)]
    dots = [MathTex(r"\cdot", font_size=30) for _ in range(3)]
    row = VGroup(parts[0], dots[0], parts[1], dots[1], parts[2], dots[2], parts[3])
    row.arrange(RIGHT, buff=0.3)
    if row.width > 13.0:
        row.scale_to_fit_width(13.0)
    row.move_to([0, FACTS_Y, 0]).set_color(DIM)
    return parts, dots


def recap_card(text, size=22, max_w=3.8, pad=0.18, lines=None):
    """kit.move_card(small=True)'s look (YELLOW rounded box, CARD_FILL, "The move" label), reflowed
    to three lines at 22 px: move_card caps at two lines, which made the row too wide."""
    lines = lines or kit._wrap(text, size, max_w)
    body = VGroup(*[kit._t(ln, size, FG) for ln in lines]).arrange(DOWN, buff=0.13 * size / 30,
                                                                   aligned_edge=LEFT)
    label = kit._t("The move", 22, YELLOW)
    inner = VGroup(label, body).arrange(DOWN, buff=0.14 * size / 30, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.12, width=inner.width + 2 * pad,
                           height=inner.height + 2 * pad)
    box.set_stroke(YELLOW, 2).set_fill(kit.CARD_FILL, 1).move_to(inner)
    card = VGroup(box, label, body)
    card.box, card.label, card.body = box, label, body
    return card


def next_rule():
    r = spr.rule_boxed().scale(1.4)
    r.move_to([N_REST, 2.35, 0])
    return r


class Recap(NarratedScene):
    def construct(self):
        self.tt = ValueTracker(0.0)
        self.add(self.tt)
        self.op_b = ValueTracker(0.0)      # both machines' opacity
        self.k_b = ValueTracker(1.0)       # their shrink at {recap}
        self.blue = ValueTracker(0.0)      # the pendulum's angle arc: YELLOW → BLUE at {rename}
        self.clip1()
        self.clip2()
        self.clip3()
        self.end_hold()

    # ── {both}: the two machines, swinging in step ─────────────────────────────
    def _both_spring(self):
        x = -B_SP_AMP * np.cos(OM * self.tt.get_value())
        g = VGroup(spr.spring_drawing(x, zero=False), spr.pull_arrow(x))
        place_spring(g, B_SP_REST, B_SP_Y, B_SP_S)
        g.scale(self.k_b.get_value(), about_point=np.array([-4.0, 0.5, 0]))
        return hook._faded(g, self.op_b.get_value())

    def _both_pendulum(self):
        th = B_PD_AMP * np.cos(OM * self.tt.get_value())
        p = grav.pendulum(th, labels=False, angle=True)
        p.remove(p.theta_label)
        p.arc.set_stroke(interpolate_color(ManimColor(YELLOW), ManimColor(BLUE), self.blue.get_value()),
                         opacity=1)
        g = VGroup(p, swing_pull(th))
        place_pendulum(g, B_PIV, B_PD_S)
        g.scale(self.k_b.get_value(), about_point=np.array([4.5, 1.5, 0]))
        return hook._faded(g, self.op_b.get_value())

    def clip1(self):
        self.tt.add_updater(lambda m, dt: m.increment_value(dt))
        self.sp_live = always_redraw(self._both_spring)
        self.pd_live = always_redraw(self._both_pendulum)
        self.leg = kit.legend(START_ENTRIES)
        rule = spr.rule_boxed().scale(1.75).move_to(RULE_AT)
        wk = omega_sq("k", "m").move_to([B_SP_REST, OMEGA_Y, 0])
        wg = omega_sq("g", "L").move_to([B_PIV[0], OMEGA_Y, 0])
        lab_pos = B_PIV + np.array([0.65, -0.5, 0])
        th_lab = MathTex(r"\theta", font_size=36, color=YELLOW).move_to(lab_pos)
        x_lab = MathTex(r"x", font_size=38, color=BLUE).move_to(lab_pos)
        tag1 = kit.tag("angular displacement x(t)").move_to([kit.EDGE_X, -1.45, 0], aligned_edge=RIGHT)
        tag2 = kit.tag("notes p. 108 · reference").move_to([kit.EDGE_X, -1.8, 0], aligned_edge=RIGHT)
        shm_t = T("simple harmonic motion", size=36, color=YELLOW).move_to(SHM_AT)
        shm_box = SurroundingRectangle(shm_t, color=YELLOW, buff=0.2).set_stroke(YELLOW, 3)
        shm_d1 = T("named by its rule", size=26, color=DIM).move_to(SHM_AT + 0.85 * DOWN)
        shm_d2 = T("its form: part two", size=26, color=DIM).move_to(SHM_AT + 1.25 * DOWN)
        self.b_static = [rule, wk, wg, x_lab, tag1, tag2]
        self.shm = (shm_t, shm_box, shm_d1, shm_d2)

        with self.say("c1.recap.1") as c:
            self.add(self.sp_live, self.pd_live)
            self.play(self.op_b.animate.set_value(1), *appear(self.leg, shift=None),  # early: the legend panel stands from the start
                      run_time=1.5)
            self.play(*appear(th_lab, shift=None), run_time=0.8)  # early: the pendulum's angle label, part of the drawing
            c.wait_until("double dot")
            self.play(*appear(rule, shift=None), run_time=1.5)
            c.wait_until("for the spring")
            self.play(*appear(wk), run_time=1.2)
            c.wait_until("for the pendulum")
            self.play(*appear(wg), run_time=1.2)

            c.wait_until("rename")
            self.play(*swap(th_lab, x_lab), self.blue.animate.set_value(1), run_time=1.5)
            c.wait_until("even when")
            kit.legend_set(self, self.leg, FINAL_ENTRIES, *appear(tag1, tag2, lag=0.3),  # early: notes tags, not read aloud
                           run_time=1.6)

            c.wait_until("shm")
            self.play(FlashAround(rule, run_time=2, time_width=1.5))
            c.wait_until("simple harmonic motion")
            self.play(*appear(shm_t, shift=None), GrowFromCenter(shm_box), run_time=1.0)
            self.play(*appear(shm_d1, shm_d2, lag=0.4), run_time=min(1.2, max(0.6, c.until() - 0.1)))  # early: the name's footnote, not read aloud

    # ── {recap}: three moves, each picture moving ──────────────────────────────
    def clip2(self):
        cards = [recap_card(S3_MOVE), recap_card(S5_MOVE), s7.math_theta(recap_card(S7_MOVE, lines=S7_LINES))]
        row = VGroup(*cards).arrange(RIGHT, buff=0.35, aligned_edge=UP)
        if row.width > 13.2:
            row.scale_to_fit_width(13.2)
        row.move_to([0, REC_TOP, 0], aligned_edge=UP)
        xs = [cd.get_center()[0] for cd in cards]
        self.cards = cards

        # m1: s3's spring, pulled out and released
        amp1, ph1, op1 = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)

        def m1_draw():
            x = amp1.get_value() * np.cos(ph1.get_value())
            g = VGroup(spr.spring_drawing(x, zero=False), spr.pull_arrow(x))
            place_spring(g, xs[0] - 0.07, REC_SP_Y, REC_SP_S)
            return hook._faded(g, op1.get_value())

        # m2: s5's pendulum, gravity split
        th2, ph2, op2, ops = ValueTracker(30.0), ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)

        def m2_draw():
            th = th2.get_value() * np.cos(ph2.get_value())
            p = hook._faded(grav.pendulum(th, labels=False, angle=False), op2.get_value())
            gs = hook._faded(grav.gravity_split(th, label=False), ops.get_value())
            g = VGroup(p, gs)
            return place_pendulum(g, [xs[1], REC_PIV_Y, 0], REC_PD_S)

        # m3: s7's arc and reach
        th3 = ValueTracker(10.0)
        m3 = s7.live_picture(th3)
        for m in m3:
            m.add_updater(lambda mob: place_pendulum(mob, [xs[2], REC_PIV_Y, 0], REC_PD_S))
            m.update()
        m3g_center = np.array([xs[2], 0.6, 0])

        parts, dots = facts_line()

        with self.say("c1.recap.2") as c:
            c.wait_until("a recap")
            gone = [m for m in self.b_static if m in self.mobjects] + [self.leg]
            shm_t, shm_box, d1, d2 = self.shm
            f = 28 / 36
            c0 = shm_box.get_center()
            c1 = np.array([0, SHM_BAND_Y, 0])
            half = shm_box.width * f / 2
            d1_to = np.array([-half - 0.35 - d1.width * 24 / 26 / 2, SHM_BAND_Y, 0])
            d2_to = np.array([half + 0.35 + d2.width * 24 / 26 / 2, SHM_BAND_Y, 0])
            self.play(*during([self.k_b.animate.set_value(0.3), self.op_b.animate.set_value(0),
                               *[FadeOut(m) for m in gone]], 0, 0.45),
                      *during([d1.animate.scale(24 / 26).move_to(d1_to),
                               d2.animate.scale(24 / 26).move_to(d2_to)], 0.25, 0.65),
                      *during([shm_t.animate.scale(f, about_point=c0).shift(c1 - c0),
                               shm_box.animate.scale(f, about_point=c0).shift(c1 - c0)], 0.55, 1),
                      run_time=max(1.6, min(2.2, c.until("m1") - 0.1)))
            self.tt.clear_updaters()
            self.remove(self.sp_live, self.pd_live)

            m1 = always_redraw(m1_draw)
            self.add(m1)
            c.wait_until("m1")
            self.play(*appear(cards[0], shift=None), op1.animate.set_value(1), run_time=1.0)  # early: the move card names the move as it is said
            c.wait_until("name the force")
            self.play(amp1.animate.set_value(3.0), run_time=1.5)
            c.wait_until("use newton")
            n = max(1, int((c.until("m2") - 0.2) * OM / TAU))
            self.play(ph1.animate.set_value(n * TAU), rate_func=linear, run_time=n * TAU / OM)

            m2 = always_redraw(m2_draw)
            self.add(m2)
            c.wait_until("m2")
            self.play(*appear(cards[1], shift=None), op2.animate.set_value(1), run_time=1.0)  # early: the move card names the move as it is said
            c.wait_until("split gravity")
            self.play(ops.animate.set_value(1), run_time=1.5)
            c.wait_until("only the swing part")
            sw = grav.gravity_split(30, label=False).swing.copy()
            place_pendulum(sw, [xs[1], REC_PIV_Y, 0], REC_PD_S)
            self.play(FlashAround(sw, run_time=1.5, time_width=1.5, color=RED))
            n = max(1, int((c.until("m3") - 0.2) * OM / TAU))
            self.play(ph2.animate.set_value(n * TAU), rate_func=linear, run_time=n * TAU / OM)

            c.wait_until("m3")
            self.play(*appear(cards[2], shift=None), *[FadeIn(m) for m in m3], run_time=1.0)  # early: the move card names the move as it is said
            c.wait_until("for small swings")
            self.play(th3.animate.set_value(60), run_time=min(3.0, c.until("because")), rate_func=smooth)
            c.wait_until("arc and the reach")
            self.play(th3.animate.set_value(10), run_time=min(3.0, c.until("facts") - 0.1), rate_func=smooth)

            c.wait_until("facts")
            for cue, piece, dot in zip(["newton's law", "hooke's law", "nine point", "arc length"],
                                       parts, [None] + dots):
                c.wait_until(cue)
                items = ([dot] if dot is not None else []) + [piece]
                self.play(*appear(*items, shift=None, lag=0.2), run_time=1.0)
        self.m_live = [m1, m2, *m3]
        self.facts = [*parts, *dots]
        self.m3_center = m3g_center

    # ── {next}: which motion? the shadow of a turning arrow ────────────────────
    def _dot_x(self):
        return N_REST + N_R * np.cos(self.ph.get_value())

    def clip3(self):
        self.ph = ValueTracker(0.0)
        self.op_n = ValueTracker(0.0)      # the turning arrow and its shadow line
        self.add(self.ph)
        line = Line([N_REST - 2.4, N_LINE_Y, 0], [N_REST + 2.4, N_LINE_Y, 0]).set_stroke(DIM, 3)
        dot = always_redraw(lambda: Dot([self._dot_x(), N_LINE_Y, 0], radius=0.14, color=BLUE).set_z_index(3))
        rule = next_rule()
        xq = MathTex(r"x(t) = \,?", font_size=56, color=YELLOW).move_to([N_TEXT_X, 0.5, 0])
        nxt = T("Next: shadows of a turning arrow", size=30, color=DIM).move_to([N_TEXT_X, -0.6, 0])
        track = Circle(radius=N_R).set_stroke(DIM, 2, opacity=0.35).move_to(N_CENTER)

        def arrow_draw():
            p = self.ph.get_value()
            tip = N_CENTER + N_R * np.array([np.cos(p), np.sin(p), 0])
            return Arrow(N_CENTER, tip, buff=0, stroke_width=5, tip_length=0.24,
                         max_tip_length_to_length_ratio=0.3, color=GOLD).set_opacity(0.6 * self.op_n.get_value())

        def shadow_draw():
            p = self.ph.get_value()
            tip = N_CENTER + N_R * np.array([np.cos(p), np.sin(p), 0])
            return DashedLine(tip, [tip[0], N_LINE_Y, 0], dash_length=0.1).set_stroke(DIM, 2.5, opacity=self.op_n.get_value())

        arrow = always_redraw(arrow_draw)
        shadow = always_redraw(shadow_draw)
        pivot = Dot(N_CENTER, radius=0.05, color=GOLD).set_opacity(0.6)
        self.n_parts = dict(line=line, dot=dot, rule=rule, xq=xq, nxt=nxt, track=track,
                            arrow=arrow, shadow=shadow, pivot=pivot)

        with self.say("c1.recap.3") as c:
            c.wait_until("which motion")
            keep = (self.ph, self.op_n, self.tt, *self.facts)
            gone = [m for m in list(self.mobjects) if m not in keep]
            self.play(*during([FadeOut(m) for m in gone], 0, 0.45),
                      *during(appear(line, dot, rule, shift=None, lag=0.2), 0.5, 1), run_time=1.8)
            self.remove(*self.m_live)
            self.ph.add_updater(lambda m, dt: m.increment_value(N_OM * dt))
            self.play(*appear(xq, shift=None), run_time=1.2)
            c.wait_until("comes back")
            self.play(FlashAround(rule, run_time=2, time_width=1.5))
            c.wait_until("arrow")
            self.add(arrow, shadow)
            self.play(*during(disappear(*self.facts), 0, 0.5),
                      FadeIn(track), FadeIn(pivot), self.op_n.animate.set_value(1), run_time=1.5)

    # ── end card, then the morph into chapter 2's first frame ──────────────────
    def end_hold(self):
        P = self.n_parts
        self.play(*appear(P["nxt"], shift=None), run_time=1.0)  # early: the end card's next-chapter line, after the last word
        self.wait(1.4)
        # let the arrow come round to point right (dot at its right end), then ease to a stop
        self.ph.clear_updaters()
        p = self.ph.get_value()
        k = int(np.ceil((p + 2.0) / TAU))
        lin_to = k * TAU - 2.0
        if lin_to - p > 0.05:
            self.play(self.ph.animate.set_value(lin_to), rate_func=linear, run_time=(lin_to - p) / N_OM)
        self.play(self.ph.animate.set_value(k * TAU), rate_func=lambda a: 1 - (1 - a) ** 2, run_time=2.0)
        self.wait(1.6)

        # freeze the live pieces
        self.ph.set_value(k * TAU)
        dot = Dot([N_REST + N_R, N_LINE_Y, 0], radius=0.14, color=BLUE).set_z_index(3)
        live = [P["dot"], P["arrow"], P["shadow"]]
        arrow = P["arrow"].copy().clear_updaters()
        shadow = P["shadow"].copy().clear_updaters()
        self.remove(*live)
        self.add(dot, arrow, shadow)

        card = ch2.opening_card()
        rest = [m for m in card.submobjects if m is not card.table and m is not card.block]
        self.play(*during(disappear(P["rule"], P["xq"], P["nxt"]), 0, 0.4),
                  *during([FadeOut(arrow), FadeOut(shadow), FadeOut(P["track"]), FadeOut(P["pivot"])], 0, 0.4),
                  *during([ReplacementTransform(P["line"], card.table),
                           ReplacementTransform(dot, card.block)], 0.3, 0.85),
                  *during([FadeIn(m) for m in rest], 0.6, 1.0),
                  run_time=2.8)
        self.remove(*[m for m in list(self.mobjects) if m not in (self.ph, self.tt, self.op_n)])
        self.add(ch2.opening_card())
        self.wait(1.2)
