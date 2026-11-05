"""Chapter 3, scene 1: three swings, one beat; can one number hold a whole swing? Title, three retrieval panels. Clips c3.hook.1 – c3.hook.3.

Shared (load_scene("ch3_s1_hook")):
  opening_card()   ch3's first frame (ch2's last): three copies of ch1's spring drawing at rest
                   (x = 0), scaled ROW_S, rest points at (REST_X, ROW_YS[i]) (table lines), plus ch2's
                   rule_pin(). VGroup(row1, row2, row3, pin).
  CLOCK = 2/3      on-screen model time per real second (the motion turns at 2 rad/s visually)
  OMEGA = 3        rad/s in the maths
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
from lib.titles import title_card  # noqa: E402

kit = load_scene("ch1_s2_tools")
spr = load_scene("ch1_s3_spring")
hook2 = load_scene("ch2_s1_hook")
ak = load_scene("ch2_s3_velocity")

# ═══════════════════════════════ shared with ch2 s9 / ch3 ═══════════════════════════════
OMEGA = 3.0
CLOCK = 2.0 / 3.0
ROW_S = 0.8                        # spring drawings scaled 0.8 (the "0" stays 22 px)
ROW_YS = [2.1, 0.4, -1.3]          # table lines of rows 1-3
REST_X = -3.92                     # rest point (the "0" tick): left edge lands at x = -6.6
_P0 = np.array([spr.SPRING_REST_X, 0.0, 0.0])


def _place(mob, s, target):
    """Map a spring drawing built at y = 0 so its rest point lands on target, scaled s."""
    mob.shift(-_P0).scale(s, about_point=ORIGIN).shift(np.array(target, dtype=float))
    return mob


def row_target(i):
    return np.array([REST_X, ROW_YS[i], 0.0])


def opening_card():
    """ch3's first frame: three spring drawings at rest, stacked down the left, and the rule pin."""
    rows = [_place(spr.spring_drawing(x=0.0, y=0.0), ROW_S, row_target(i)) for i in range(3)]
    return VGroup(*rows, hook2.rule_pin())


# ═══════════════════════════════ scene layout ═══════════════════════════════
DRAW = 0.7                          # drawing cm per cm of displacement (5 cm keeps clear of the wall)
AMPS = [4.0, 2.0, 5.0]              # each swing's size, cm
STRIP_S = 0.36                      # rows shrunk into the bottom strip
STRIP_XS = [-4.7, 0.0, 4.7]
STRIP_Y = -3.3
AXIS_UP = 0.4 * ROW_S               # the time axis sits at the block's centre height
WX0 = -0.55                         # time axis t = 0
WSEC = 0.85                         # time-axis units per model second
WS = 0.15                           # wave units per cm
PERIOD = 2 * PI / OMEGA             # 2.094 s
TW = 2 * PERIOD                     # two periods on each axis
FORM_X = 5.15                       # centre of the formula column
PANEL_C = np.array([0.0, -0.7, 0.0])
SLOTS = [np.array([-4.55, 2.15, 0.0]), np.array([3.6, 2.15, 0.0])]
SLOT_S = 0.6

E_X = (r"x", BLUE, "displacement")
E_T = (r"t", FG, "time")
E_OM = (r"\omega", FG, "= 3 rad/s")
E_A = (r"a", BLUE, "cosine coefficient")
E_B = (r"b", BLUE, "sine coefficient")


def x_of(i, tau):
    w = OMEGA * tau
    return [4 * np.cos(w), 2 * np.sin(w), 3 * np.cos(w) + 4 * np.sin(w)][i]


def axis_y(i):
    return ROW_YS[i] + AXIS_UP


def wave_pt(i, tau):
    return np.array([WX0 + WSEC * tau, axis_y(i) + WS * x_of(i, tau), 0.0])


def _opacity(g, op):
    for m in g.family_members_with_points():
        m.set_stroke(opacity=m.get_stroke_opacity() * op)
        m.set_fill(opacity=m.get_fill_opacity() * op)
    return g


def _frame(content, buff=0.32):
    box = RoundedRectangle(corner_radius=0.12, width=content.width + 2 * buff,
                           height=content.height + 2 * buff)
    box.set_stroke(DIM, 1.5).set_fill(kit.CARD_FILL, 0.95).move_to(content).set_z_index(-5)
    return box


def _axes(o, left, right, down, up):
    o = np.array(o, dtype=float)
    g = VGroup(Line(o + left * LEFT, o + right * RIGHT), Line(o + down * DOWN, o + up * UP))
    return g.set_stroke(DIM, 2.5).set_z_index(-3)


def _right_angle(o, d1, d2, s=0.18):
    o = np.array(o, dtype=float)
    return VMobject().set_points_as_corners([o + s * d1, o + s * (d1 + d2), o + s * d2]).set_stroke(FG, 2.5)


def _unit(deg):
    a = deg * DEGREES
    return np.array([np.cos(a), np.sin(a), 0.0])


# ── the retrieval panels (built at the panel centre) ──
def panel_sine():
    o = PANEL_C + np.array([-1.75, 0, 0])
    R = 1.0
    ax = _axes(o, 1.3, 1.3, 1.3, 1.3)
    circ = Circle(radius=R).move_to(o).set_stroke(DIM, 2.5).set_z_index(-3)
    w0 = PANEL_C + np.array([0.15, 0, 0])
    tax = Line(w0, w0 + 3.0 * RIGHT).set_stroke(DIM, 2.5)
    ss = np.linspace(0, 2 * PI, 80)
    wave = VMobject().set_points_as_corners([w0 + np.array([2.7 * s / (2 * PI), R * np.sin(s), 0]) for s in ss])
    wave.set_stroke(BLUE, 4)
    lab = MathTex(r"\sin\omega t", font_size=40, color=BLUE).move_to(w0 + np.array([2.05, 0.62, 0]))
    q = T("?", size=48, color=YELLOW).move_to(o + np.array([0.42, 0.42, 0]))
    arrow = ak.arrow_between(o, o + R * DOWN, GOLD)
    mi = MathTex("-i", font_size=40, color=PINK).next_to(arrow.get_end(), RIGHT, buff=0.15)
    dot = Dot(o, radius=0.09, color=BLUE).set_z_index(1)
    content = VGroup(ax, circ, tax, wave, lab, q, mi)
    frame = _frame(VGroup(content, arrow))
    g = VGroup(frame, ax, circ, tax, wave, lab)
    g.q, g.arrow, g.mi, g.dot = q, arrow, mi, dot
    return g


def panel_deriv():
    o = PANEL_C + np.array([-2.6, -0.45, 0])
    R = 0.9
    ax = _axes(o, 1.15, 1.25, 0.55, 1.45)
    circ = Circle(radius=R).move_to(o).set_stroke(DIM, 2.5).set_z_index(-3)
    d1, d2 = _unit(20), _unit(110)
    gold = ak.arrow_between(o, o + R * d1, GOLD)
    green = ak.arrow_between(o, o + 1.5 * R * d2, GREEN)
    ra = _right_angle(o, d1, d2)
    lhs = MathTex(r"\dfrac{d}{dt}\,", r"e^{i\omega t}", "=", font_size=46)
    lhs[1].set_color(GOLD)
    lhs.move_to(PANEL_C + np.array([0.45, 0.0, 0]))
    ans = MathTex("i", r"\omega", r"\,e^{i\omega t}", font_size=46)
    ans[0].set_color(PINK)
    ans[2].set_color(GREEN)
    ans.next_to(lhs, RIGHT, buff=0.2)
    ans.align_to(lhs[1], DOWN)
    q = T("?", size=48, color=YELLOW).next_to(lhs, RIGHT, buff=0.25)
    frame = _frame(VGroup(ax, circ, gold, green, lhs, ans))
    g = VGroup(frame, ax, circ, gold, lhs)
    g.q, g.green, g.ra, g.ans = q, green, ra, ans
    return g


def panel_modulus():
    u = 0.36
    o = PANEL_C + np.array([-3.0, -1.0, 0])
    grid = VGroup(*[Line(o + [x * u, 0, 0], o + [x * u, 4.5 * u, 0]) for x in range(1, 5)],
                  *[Line(o + [0, y * u, 0], o + [4.5 * u, y * u, 0]) for y in range(1, 5)])
    grid.set_stroke(DIM, 1, opacity=0.4).set_z_index(-4)
    ax = _axes(o, 0.3, 4.7 * u, 0.3, 4.9 * u)
    p = o + np.array([3 * u, 4 * u, 0])
    dot = Dot(p, radius=0.09, color=YELLOW)
    plab = MathTex("3", "+", "4", "i", font_size=38).next_to(p, RIGHT, buff=0.15)
    plab[3].set_color(PINK)
    lhs = MathTex("|", "3", "+", "4", "i", "|", "=", font_size=48)
    lhs[4].set_color(PINK)
    lhs.move_to(PANEL_C + np.array([1.3, 0.0, 0]))
    five = MathTex("5", font_size=48, color=GOLD).next_to(lhs, RIGHT, buff=0.22)
    q = T("?", size=48, color=YELLOW).next_to(lhs, RIGHT, buff=0.25)
    hyp = ak.arrow_between(o, p, GOLD, width=5)
    leg_re = Line(o, o + 3 * u * RIGHT).set_stroke(BLUE, 6)
    leg_im = Line(o + 3 * u * RIGHT, p).set_stroke(PINK, 6)
    l3 = MathTex("3", font_size=38, color=BLUE).next_to(leg_re, DOWN, buff=0.15)
    l4 = MathTex("4", font_size=38, color=PINK).next_to(leg_im, RIGHT, buff=0.15)
    l5 = MathTex("5", font_size=38, color=GOLD).move_to((o + p) / 2 + 0.3 * _unit(143))
    frame = _frame(VGroup(grid, ax, plab, lhs, five, l3, l4, dot), buff=0.4)
    g = VGroup(frame, grid, ax, dot, plab, lhs)
    g.q, g.five, g.hyp, g.l5, g.legs, g.labs = q, five, hyp, l5, [leg_re, leg_im], [l3, l4]
    return g


class Hook(NarratedScene):
    def construct(self):
        oc = opening_card()
        self.add(*oc)
        pin = oc[3]
        # the chapter clock: model time runs at CLOCK of real time
        self.tm = ValueTracker(0.0)
        self.tm.add_updater(lambda m, dt: m.increment_value(CLOCK * dt))
        self.pre = [ValueTracker(0.0) for _ in range(3)]
        self.u = [ValueTracker(0.0) for _ in range(3)]
        self.op = ValueTracker(1.0)
        self.start = [None, None, None]
        self.add(self.tm, *self.pre, *self.u, self.op)
        self.zeros = [r.zero for r in oc[:3]]
        self.rows = [always_redraw(lambda i=i: self.row(i)) for i in range(3)]
        self.remove(*oc[:3])
        self.add(*self.rows, *self.zeros)   # the "0" labels stay put as their own objects
        self.trackers = [self.tm, *self.pre, *self.u, self.op]

        self.clip1()
        self.clip2(pin)
        self.clip3(pin)

        self.play(self.op.animate.set_value(0.0),
                  *[FadeOut(m) for m in self.mobjects if m not in self.rows and m not in self.trackers],
                  run_time=1.0)
        self.remove(*self.rows)
        self.wait(0.15)

    # ── the three rows: one clock ──
    def disp(self, i):
        if self.start[i] is None:
            return self.pre[i].get_value()
        return x_of(i, self.tm.get_value() - self.start[i])

    def row(self, i):
        u = self.u[i].get_value()
        s = ROW_S + (STRIP_S - ROW_S) * u
        target = (1 - u) * row_target(i) + u * np.array([STRIP_XS[i], STRIP_Y, 0.0])
        g = spr.spring_drawing(DRAW * self.disp(i), 0.0, zero=False)
        _place(g, s, target)
        op = self.op.get_value()
        if op < 1:
            _opacity(g, op)
        return g

    def tau(self, i):
        if self.start[i] is None:
            return 0.0
        return float(np.clip(self.tm.get_value() - self.start[i], 0.0, TW))

    def wave(self, i):
        t1 = self.tau(i)
        if t1 < 0.02:
            return VMobject()
        ts = np.linspace(0, t1, max(3, int(t1 / 0.02) + 1))
        return VMobject().set_points_as_corners([wave_pt(i, t) for t in ts]).set_stroke(BLUE, 4)

    def front(self, i):
        t1 = self.tau(i)
        d = Dot(wave_pt(i, t1), radius=0.07, color=BLUE)
        return d.set_opacity(0 if t1 >= TW - 1e-3 else 1)

    def time_axes(self, i):
        ay, a = axis_y(i), AMPS[i] * WS + 0.15
        tl = Line([WX0 - 0.05, ay, 0], [WX0 + WSEC * TW + 0.3, ay, 0]).set_stroke(DIM, 2)
        xl = Line([WX0, ay - a, 0], [WX0, ay + a, 0]).set_stroke(DIM, 2)
        t = MathTex("t", font_size=30, color=DIM).next_to(tl, RIGHT, buff=0.1)
        return VGroup(tl, xl, t)

    def release(self, i):
        self.start[i] = self.tm.get_value()
        w = always_redraw(lambda: self.wave(i))
        f = always_redraw(lambda: self.front(i))
        self.add(w, f)
        return w, f

    def start_label(self, i, text):
        lab = T(text, size=26, color=DIM)
        lab.move_to([REST_X, ROW_YS[i] + 0.85, 0])
        return lab

    # ── clip 1: three swings, one beat ──
    def clip1(self):
        with self.say("c3.hook.1") as c:
            self.leg = kit.legend([E_X, E_T, E_OM], max_rows=3)
            self.play(*appear(self.leg), run_time=min(1.2, c.until("The first")))  # early: the legend opens with the scene
            c.wait_until("The first")
            self.axes = [self.time_axes(i) for i in range(3)]
            self.play(self.pre[0].animate.set_value(4.0), *appear(self.axes[0], shift=None),
                      run_time=min(1.8, 0.9 * c.until("let go")))
            c.wait_until("let go")
            self.waves = [self.release(0)]
            l1 = self.start_label(0, "let go from 4 cm")
            self.play(*appear(l1), run_time=1.0)
            c.wait_until("second")
            self.waves.append(self.release(1))
            l2 = self.start_label(1, "pushed from the middle")
            self.play(*appear(self.axes[1], shift=None), run_time=0.8)
            c.wait_until(own_word=l2)
            self.play(*appear(l2), run_time=1.0)
            c.wait_until("third")
            self.play(self.pre[2].animate.set_value(3.0), *appear(self.axes[2], shift=None),
                      run_time=min(1.5, 0.9 * c.until("already")))
            c.wait_until("already")
            self.waves.append(self.release(2))
            l3 = self.start_label(2, "3 cm out, moving out")
            self.play(*appear(l3), run_time=1.0)
            self.labels = [l1, l2, l3]

            # {beat}: one period, the same length on every axis
            c.wait_until("beat")
            self.braces = [span_brace(np.array([WX0, axis_y(i) - AMPS[i] * WS, 0]),
                                      np.array([WX0 + WSEC * PERIOD, axis_y(i) - AMPS[i] * WS, 0]),
                                      DOWN, TEAL, inset=0.0, buff=0.14) for i in range(3)]
            per = MathTex(r"T = 2\pi/3 \approx 2.09\ \text{s}", font_size=30, color=TEAL)
            per.next_to(self.braces[0], RIGHT, buff=0.25)
            self.per = per
            self.play(*[GrowFromCenter(b) for b in self.braces], run_time=1.2)
            self.play(*appear(per), run_time=0.8)

            # {differ}: crest heights, then first-crest times
            c.wait_until("differ")
            self.hticks = VGroup()
            for i in range(3):
                y = axis_y(i) + AMPS[i] * WS
                tk = Line([WX0 - 0.1, y, 0], [WX0 + 0.1, y, 0]).set_stroke(YELLOW, 4)
                lab = MathTex(f"{AMPS[i]:.0f}", font_size=30, color=YELLOW).next_to(tk, LEFT, buff=0.08)
                self.hticks.add(VGroup(tk, lab))
            self.play(*appear(*self.hticks, shift=None, lag=0.3), run_time=1.2)
            c.wait_until("shifted")
            crest = [0.0, PI / 2 / OMEGA, np.arctan2(4, 3) / OMEGA]
            self.cticks = VGroup()
            for i in range(3):
                p = wave_pt(i, crest[i])
                base = np.array([p[0], axis_y(i), 0])
                self.cticks.add(VGroup(DashedLine(p, base, dash_length=0.06).set_stroke(YELLOW, 2.5),
                                       Dot(p, radius=0.08, color=YELLOW),
                                       Line(base + 0.1 * DOWN, base + 0.1 * UP).set_stroke(YELLOW, 4)))
            self.play(*appear(*self.cticks, shift=None, lag=0.3), run_time=min(1.2, c.until(floor=0.6)))

    # ── clip 2: two numbers per swing; derivatives swap them ──
    def clip2(self, pin):
        with self.say("c3.hook.2", gap=3.2) as c:
            specs = [(["x", "=", "4", r"\cos 3t"], [2], r"(a, b) = (4, 0)"),
                     (["x", "=", "2", r"\sin 3t"], [2], r"(a, b) = (0, 2)"),
                     (["x", "=", "3", r"\cos 3t", "+", "4", r"\sin 3t"], [2, 5], r"(a, b) = (3, 4)")]
            self.forms = []
            for i, (parts, blue, pair) in enumerate(specs):
                f = MathTex(*parts, font_size=32)
                f[0].set_color(BLUE)
                for k in blue:
                    f[k].set_color(BLUE)
                p = MathTex(pair, font_size=28, color=BLUE)
                g = VGroup(f, p).arrange(DOWN, buff=0.16).move_to([FORM_X, axis_y(i), 0])
                self.forms.append(g)
            self.play(*appear(*self.forms, lag=0.35), run_time=min(2.2, c.until("cosine coefficient")))
            c.wait_until("cosine coefficient")
            kit.legend_add(self, self.leg, E_A, E_B, run_time=1.2)

            # {swap}: differentiate row 3's swing
            c.wait_until("swap")
            d = MathTex(r"\dfrac{d}{dt}", r"\Big(", "3", r"\cos", "3t", "+", "4", r"\sin", "3t", r"\Big)",
                        "=", "-9", r"\sin", "3t", "+", "12", r"\cos", "3t", font_size=32)
            for k in range(11, 18):
                d[k].set_color(GREEN)
            d.move_to([2.95, -2.75, 0])
            self.deriv = d
            olds = [*self.braces, self.per, *self.hticks, *self.cticks]
            self.play(*during(disappear(*olds), 0, 0.4), *during(appear(d), 0.45, 1),
                      run_time=min(2.0, c.until("into sines")))
            c.wait_until("into sines")
            a1 = CurvedArrow(d[3].get_top() + 0.08 * UP, d[12].get_top() + 0.08 * UP, angle=-PI / 3,
                             color=YELLOW, stroke_width=3, tip_length=0.18)
            self.play(Create(a1), d[3].animate.set_color(YELLOW), d[12].animate.set_color(YELLOW),
                      run_time=1.2)
            c.wait_until("and the sines")
            a2 = CurvedArrow(d[7].get_bottom() + 0.08 * DOWN, d[16].get_bottom() + 0.08 * DOWN, angle=PI / 3,
                             color=YELLOW, stroke_width=3, tip_length=0.18)
            self.play(Create(a2), d[7].animate.set_color(YELLOW), d[16].animate.set_color(YELLOW),
                      run_time=1.2)

            # {question}: clear to the swinging rows as the question is asked, then the title
            q = T("Can one number hold\na whole swing?", size=46, color=YELLOW, line_spacing=1.0)
            q.move_to([2.8, 2.35, 0])
            self.q = q
            for w, f in self.waves:
                w.clear_updaters()
                f.clear_updaters()
            self.remove(*[f for _, f in self.waves])
            c.wait_until("this part")
            sweep_clear(self, *during(appear(q), 0.55, 1), keep=[*self.rows, *self.zeros, pin, *self.trackers],
                        run_time=min(2.4, c.until("whole swing") + 0.4))
            card = title_card("Part 3 · The complex amplitude")
            card.move_to([2.9, -1.1, 0])
            self.card = card
            c.wait_until("whole swing")
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),
                      run_time=min(1.2, max(0.5, c.until() - 0.2)))  # early: title card
            self.play(*appear(card.course, card.part, lag=0.4), run_time=1.2)  # early: title card

    # ── clip 3: three quick retrieval questions ──
    def clip3(self, pin):
        card = self.card
        with self.say("c3.hook.3", gap=1.5) as c:
            c.wait_until("questions")
            self.play(*during(disappear(self.q, card.title, card.rule, card.course, card.part, *self.zeros), 0, 0.4),
                      *during([self.u[2].animate.set_value(1.0)], 0.2, 0.7),
                      *during([self.u[1].animate.set_value(1.0)], 0.35, 0.85),
                      *during([self.u[0].animate.set_value(1.0)], 0.5, 1.0),
                      run_time=min(2.4, c.until("q1")))
            # q1 / a1
            c.wait_until("q1")
            p1 = panel_sine()
            self.play(*appear(p1, p1.q, lag=0.3), run_time=1.2)
            c.wait_until("a1")
            self.play(*during(disappear(p1.q), 0, 0.35), *during([GrowArrow(p1.arrow)], 0.3, 0.85),
                      *during(appear(p1.mi, p1.dot, shift=None, lag=0.3), 0.6, 1), run_time=1.8)
            settle(self, p1, add=[p1.arrow, p1.mi, p1.dot])
            # q2 / a2
            c.wait_until("q2")
            p2 = panel_deriv()
            self.play(*during([p1.animate.scale(SLOT_S).move_to(SLOTS[0])], 0, 0.6),
                      *during(appear(p2, p2.q, shift=None, lag=0.3), 0.55, 1), run_time=2.0)
            c.wait_until("a2")
            self.play(*swap(p2.q, p2.ans), *during([GrowArrow(p2.green)], 0.3, 0.85),
                      *during([Create(p2.ra)], 0.7, 1), run_time=1.8)
            settle(self, p2, add=[p2.ans, p2.green, p2.ra])
            # q3 / a3
            c.wait_until("q3")
            p3 = panel_modulus()
            self.play(*during([p2.animate.scale(SLOT_S).move_to(SLOTS[1])], 0, 0.6),
                      *during(appear(p3, p3.q, shift=None, lag=0.3), 0.55, 1), run_time=2.0)
            c.wait_until("a3")
            self.play(*swap(p3.q, p3.five), *during([GrowArrow(p3.hyp)], 0.2, 0.8),
                      *during(appear(p3.l5, shift=None), 0.6, 1), run_time=1.4)
            self.play(*[Create(l) for l in p3.legs], *appear(*p3.labs, shift=None, lag=0.3), run_time=1.2)
            c.wait_until()
