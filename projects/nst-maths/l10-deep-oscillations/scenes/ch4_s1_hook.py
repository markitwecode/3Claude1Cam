"""Chapter 4, scene 1: hook (a hanging spring bobs, freeze, "is that enough?"), title, three
retrieval questions. Clips c4.hook.1 – c4.hook.3.

Exports for the rest of chapter 4 (load_scene("ch4_s1_hook")); signatures are stable:
  hanging_spring(x=7, pos=None, scale=1.0)  DIM hatched ceiling, ch1's FG coil, ch1's BLUE block.
                       x = F19's position in cm, measured upward (rest 7, range -18..32).
                       pos = the weight's centre at rest (x = 7); default HANG_REST (-3.2, 0).
                       Everything scales about pos. .ceiling .hatch .coil .weight
  weight_center(x=7, pos=None, scale=1.0)   centre of the weight at position x
  ceiling_y(pos=None, scale=1.0)            y of the ceiling line
  opening_card()       ch4's first frame (ch3's last): hanging_spring(7) alone, centred on x = -3.2
  amp_pin()            the chapter's pin x(t) = Re[A e^{iωt}] (kit.pinned at the pin slot)
Geometry at scale 1: ceiling line y = 3.1 (hatch to 3.32), weight 0.9 x 0.8, rest centre
(-3.2, -0.3), 0.06 scene units per cm (x = 32 -> centre y 1.2, coil 1.5 long; x = -18 -> centre
y -1.8, bottom -2.2). Coil: 6 turns.
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

# ═══════════════════════════════ the hanging spring (shared) ═══════════════════════════════
X_REST = 7.0                                     # F19: centre of the motion (cm, upward)
HANG_REST = np.array([spr.SPRING_REST_X, -0.3, 0])  # weight centre at x = 7 (scale 1)
HANG_UNIT = 0.06                                 # scene units per cm
CEIL_DY = 3.4                                    # ceiling line this far above HANG_REST
CEIL_W = 1.8                                     # ceiling width
BLOCK_W, BLOCK_H = spr.BLOCK_W, spr.BLOCK_H


def _pos(pos):
    return HANG_REST.copy() if pos is None else np.array(pos, dtype=float)


def weight_center(x=X_REST, pos=None, scale=1.0):
    """Centre of the weight at F19 position x (cm, upward)."""
    return _pos(pos) + scale * HANG_UNIT * (x - X_REST) * UP


def ceiling_y(pos=None, scale=1.0):
    return _pos(pos)[1] + scale * CEIL_DY


def _vcoil(xc, y0, y1, turns=6, amp=0.2, lead=0.22, width=3):
    """ch1's coil, vertical: from y0 (top) down to y1."""
    pts = [[xc, y0, 0], [xc, y0 - lead, 0]]
    n = 2 * turns
    span = max(y0 - y1 - 2 * lead, 0.05)
    for i in range(n):
        t = (i + 0.5) / n
        pts.append([xc + (amp if i % 2 == 0 else -amp), y0 - lead - t * span, 0])
    pts += [[xc, y1 + lead, 0], [xc, y1, 0]]
    return VMobject().set_points_as_corners(pts).set_stroke(FG, width)


def hanging_spring(x=X_REST, pos=None, scale=1.0):
    """The spring hung from a DIM hatched ceiling, the BLUE weight at position x (cm, upward)."""
    p = _pos(pos)
    s = scale
    cy = ceiling_y(p, s)
    xc = p[0]
    ceiling = Line([xc - s * CEIL_W / 2, cy, 0], [xc + s * CEIL_W / 2, cy, 0]).set_stroke(DIM, 4)
    hatch = VGroup(*[Line([xc - s * CEIL_W / 2 + s * (0.1 + 0.25 * i), cy, 0],
                          [xc - s * CEIL_W / 2 + s * (0.32 + 0.25 * i), cy + s * 0.22, 0])
                     for i in range(7)]).set_stroke(DIM, 2)
    c = weight_center(x, p, s)
    weight = Rectangle(width=s * BLOCK_W, height=s * BLOCK_H).set_stroke(BLUE, 3).set_fill(BLUE, 0.3)
    weight.move_to(c)
    coil = _vcoil(xc, cy, c[1] + s * BLOCK_H / 2, amp=0.2 * s, lead=0.22 * s, width=3 if s >= 0.6 else 2)
    g = VGroup(hatch, ceiling, coil, weight)
    g.ceiling, g.hatch, g.coil, g.weight = ceiling, hatch, coil, weight
    return g


def opening_card():
    """ch4's first frame (and ch3's last): the hanging spring alone, at rest, centred on x = -3.2."""
    return hanging_spring(X_REST)


PIN_TEX = r"x(t) = \mathrm{Re}\left[\,A\,e^{i\omega t}\,\right]"


def amp_pin():
    """The chapter's pin x(t) = Re[A e^{iωt}]: x(t), Re BLUE; A, e^{iωt} GOLD. .formula .label"""
    try:
        ch3 = load_scene("ch3_s2_freeze")
        if hasattr(ch3, "amp_pin"):
            return ch3.amp_pin()
    except Exception:
        pass
    p = kit.pinned(PIN_TEX)
    f = p.formula[0]
    # glyphs: x ( t ) = R e [ A e i ω t ]
    for i in (0, 1, 2, 3, 5, 6):
        f[i].set_color(BLUE)
    for i in (8, 9, 10, 11, 12):
        f[i].set_color(GOLD)
    return p




# ═══════════════════════════════ this scene ═══════════════════════════════
ak = load_scene("ch2_s3_velocity")
pend = load_scene("ch1_s5_gravity")

W3 = 3.0                       # F19's ω
PERIOD = TAU / W3
T_LOW = -0.9526                # F19's lowest point (x = -18) before t = 0
SEC = 0.8                      # time axis: scene units per second
AX0, AX1 = -1.5, 6.0           # time axis span (at the rest level, HANG_REST y)
PEN0 = -1.15                   # pen x when the trace starts
V_SCALE = 0.05                 # velocity arrow: scene units per cm/s
COL_X = [-4.5, 0.0, 4.5]       # retrieval columns
Q_Y = 2.25                     # question line
Q2_Y = 1.7                     # second question line
RULE_Y = -2.6                 # caption line under each picture


def f19(t):
    return 7 + 24 * np.cos(W3 * t) + 7 * np.sin(W3 * t)


def f19_v(t):
    return -72 * np.sin(W3 * t) + 21 * np.cos(W3 * t)


def height(x):
    return weight_center(x)[1]


def _dim(m, op):
    for sm in m.family_members_with_points():
        sm.set_stroke(opacity=op * (sm.get_stroke_opacity() > 0))
        sm.set_fill(opacity=op * (sm.get_fill_opacity() > 0))
    return m


def _mt(tex, size=34, color=FG, **kw):
    return MathTex(tex, font_size=size, color=color, **kw)


class Hook(NarratedScene):
    def construct(self):
        st = {"run": False, "t_tr": None, "t_end": None}
        xt = ValueTracker(X_REST)          # weight position before the release
        tt = ValueTracker(T_LOW)           # F19 time once it runs
        op = ValueTracker(1.0)             # brightness of the trace side
        pen_op = ValueTracker(0.0)         # the pen fades in with the axis

        def X():
            return f19(tt.get_value()) if st["run"] else xt.get_value()

        def pen_x(t):
            return PEN0 + SEC * (t - st["t_tr"])

        def t_now():
            t = tt.get_value()
            return min(t, st["t_end"]) if st["t_end"] is not None else t

        clock = lambda m, dt: m.increment_value(dt)  # noqa: E731

        card = opening_card()
        self.add(card)
        spring = always_redraw(lambda: hanging_spring(X()))

        def wave_build():
            t0, t1 = st["t_tr"], t_now()
            if t1 - t0 < 0.02:
                return VMobject()
            ts = np.linspace(t0, t1, max(3, int((t1 - t0) / 0.01) + 1))
            pts = [[pen_x(t), height(f19(t)), 0] for t in ts]
            return VMobject().set_points_as_corners(pts).set_stroke(BLUE, 4, opacity=op.get_value())

        def pen_build():
            t = t_now()
            y = height(X())
            p = np.array([pen_x(t), y, 0])
            line = DashedLine([HANG_REST[0] + BLOCK_W / 2, y, 0], p, dash_length=0.08)
            k = op.get_value() * pen_op.get_value()
            line.set_stroke(FG, 1.5, opacity=0.35 * k)
            dot = Dot(p, radius=0.08, color=BLUE).set_opacity(k)
            return VGroup(line, dot)

        # ── c4.hook.1: the phenomenon ────────────────────────────────────────
        with self.say("c4.hook.1") as c:
            c.wait_until("pull it down")
            self.remove(card)
            self.add(spring)
            pull_rt = 1.4
            self.play(xt.animate.set_value(-18), run_time=pull_rt)
            # release at F19's lowest point, k periods before t = 0 lands on {freeze}
            t_fr = c.at("freeze")
            k = 0
            while t_fr - (abs(T_LOW) + (k + 1) * PERIOD) >= self.time + 0.4:
                k += 1
            t0 = T_LOW - k * PERIOD
            rel = t_fr - abs(t0)
            if rel > self.time:
                self.wait(rel - self.time)
            tt.set_value(t0)
            st["run"] = True
            tt.add_updater(clock)
            self.add(tt)

            level = DashedLine([HANG_REST[0] - 1.1, HANG_REST[1], 0], [HANG_REST[0] + 1.1, HANG_REST[1], 0],
                               dash_length=0.12).set_stroke(DIM, 2.5)
            rest_lab = T("at rest", size=28, color=DIM).next_to(level, LEFT, buff=0.2)
            c.wait_until("bob")
            self.play(Create(level), run_time=1.0)
            c.wait_until(own_word=rest_lab)
            self.play(*appear(rest_lab), run_time=0.9)

            axis = Arrow([AX0, HANG_REST[1], 0], [AX1 + 0.25, HANG_REST[1], 0], buff=0, stroke_width=2.5, tip_length=0.18,
                         max_tip_length_to_length_ratio=0.05, color=DIM)
            t_lab = MathTex("t", font_size=34, color=DIM).next_to(axis.get_end(), DOWN, buff=0.15)
            c.wait_until("trace")
            st["t_tr"] = tt.get_value()
            st["t_end"] = st["t_tr"] + (AX1 - PEN0) / SEC
            wave = always_redraw(wave_build)
            pen = always_redraw(pen_build)
            self.add(wave, pen)
            self.play(GrowArrow(axis), FadeIn(t_lab), pen_op.animate.set_value(1.0), run_time=1.0)

            c.wait_until("freeze")
            tt.clear_updaters()
            tt.set_value(0.0)
            self.wait(0.05)

            y0 = height(f19(0))
            dot = Dot([HANG_REST[0], y0, 0], radius=0.11, color=BLUE).set_z_index(3)
            where = T("where it starts", size=30, color=BLUE)
            where.next_to(HANG_REST * RIGHT + y0 * UP + LEFT * (BLOCK_W / 2), LEFT, buff=0.25)
            c.wait_until("where it is")
            self.play(GrowFromCenter(dot), *appear(where, shift=0.2 * RIGHT), run_time=1.2)

            ax_x = HANG_REST[0] + BLOCK_W / 2 + 0.3
            vel = Arrow([ax_x, y0, 0], [ax_x, y0 + V_SCALE * f19_v(0), 0], buff=0, stroke_width=6,
                        tip_length=0.24, max_tip_length_to_length_ratio=0.3, color=GREEN)
            fast = T("how fast", size=30, color=GREEN).next_to(vel.get_end(), RIGHT, buff=0.2)
            fast.shift(0.15 * DOWN)
            c.wait_until("how fast")
            self.play(GrowArrow(vel), *appear(fast, shift=0.2 * LEFT), run_time=1.2)

            ts = np.linspace(0, st["t_end"], 400)
            fut = VMobject().set_points_as_corners([[pen_x(t), height(f19(t)), 0] for t in ts])
            future = DashedVMobject(fut, num_dashes=90).set_stroke(DIM, 3)
            qmark = T("?", size=72, color=YELLOW).move_to([(pen_x(0) + AX1) / 2 + 0.4, 2.45, 0])
            c.wait_until("question")
            self.play(Create(future), run_time=min(1.8, 0.5 * c.until()))
            self.play(*appear(qmark), run_time=1.0)

        # ── c4.hook.2: title, then retrieval q1 ─────────────────────────────
        with self.say("c4.hook.2") as c:
            card_t = title_card("Part 4 · Putting it to work")
            card_t.scale(0.8).move_to([2.75, 0.15, 0])
            tt.add_updater(clock)
            self.play(*during(disappear(dot, where, vel, fast, qmark), 0, 0.45),
                      *during([restyle(future, op=0.0), restyle(axis, op=0.08), restyle(t_lab, op=0.0),
                               op.animate.set_value(0.08)], 0, 0.5),
                      *during([FadeIn(card_t.title, shift=0.3 * DOWN), GrowFromCenter(card_t.rule)], 0.45, 1),
                      run_time=1.6)  # early: title card
            self.play(*appear(card_t.course, card_t.part, lag=0.3), run_time=0.9)  # early: title card

            pin = amp_pin()
            c.wait_until("recall")
            tt.clear_updaters()
            for m in (spring, wave, pen):
                m.clear_updaters()
            sweep_clear(self, *appear(pin, shift=0.2 * DOWN), run_time=1.6)

            # q1
            q1 = _mt(r"3\cos 3t + 4\sin 3t", size=40)
            q1[0][0].set_color(BLUE)
            q1[0][7].set_color(BLUE)
            q1.move_to([COL_X[0], Q_Y, 0])
            q1b = T("its complex amplitude?", size=28).move_to([COL_X[0], Q2_Y, 0])
            c.wait_until("q1")
            self.play(*appear(q1, q1b, lag=0.4), run_time=1.4)

            o1 = np.array([COL_X[0] - 0.85, 0.7, 0])
            u1 = 0.6
            axes1 = VGroup(Line(o1 + LEFT * 0.5, o1 + RIGHT * (3 * u1 + 0.6)),
                           Line(o1 + DOWN * (4 * u1 + 0.4), o1 + UP * 0.4)).set_stroke(DIM, 2)
            re1 = T("Re", size=24, color=DIM).next_to(axes1[0].get_end(), RIGHT, buff=0.12)
            im1 = T("Im", size=24, color=DIM).next_to(axes1[1].get_end(), LEFT, buff=0.12)
            p3 = o1 + RIGHT * 3 * u1
            p34 = p3 + DOWN * 4 * u1
            a3 = ak.arrow_between(o1, p3, BLUE, width=6)
            a4 = ak.arrow_between(p3, p34, PINK, width=6)
            aA = ak.arrow_between(o1, p34, GOLD, width=6)
            l3 = _mt("3", 32, BLUE).next_to(a3, UP, buff=0.12)
            l4 = _mt("-4i", 32, PINK).next_to(a4, RIGHT, buff=0.15)
            lA = _mt("3 - 4i", 36, GOLD).next_to(p34, LEFT, buff=0.2).shift(0.2 * DOWN)
            c.wait_until("a1")
            self.play(FadeIn(axes1), FadeIn(re1), FadeIn(im1), GrowArrow(a3), FadeIn(l3), run_time=0.9)
            self.play(GrowArrow(a4), FadeIn(l4), run_time=0.8)
            self.play(GrowArrow(aA), *appear(lA), run_time=1.0)

            rule1 = _mt(r"a\cos + b\sin \;\to\; A = a - ib", 34)
            for i in (0, 5):
                rule1[0][i].set_color(BLUE)
            rule1[0][10].set_color(GOLD)
            rule1[0][12].set_color(BLUE)
            rule1[0][14].set_color(PINK)
            rule1[0][15].set_color(BLUE)
            rule1.move_to([COL_X[0], RULE_Y, 0])
            c.wait_until("cosine coefficient")
            self.play(*appear(rule1), run_time=1.0)

        col1 = [q1, q1b, axes1, re1, im1, a3, a4, aA, l3, l4, lA, rule1]

        # ── c4.hook.3: q2, q3 ─────────────────────────────────────────────────
        with self.say("c4.hook.3") as c:
            q2 = T("its velocity's", size=28).move_to([COL_X[1], Q_Y, 0])
            q2b = T("complex amplitude?", size=28).move_to([COL_X[1], Q2_Y, 0])
            o2 = np.array([COL_X[1] - 0.2, -1.2, 0])
            sc = 1.0 / ak.PLANE_R          # 1 value unit = 1 scene unit
            ang = 15 * DEGREES
            axes2 = VGroup(Line(o2 + LEFT * 1.6, o2 + RIGHT * 1.6),
                           Line(o2 + DOWN * 0.5, o2 + UP * 2.3)).set_stroke(DIM, 2)
            gA = ak.turning_arrow(0.0, offset=ang, length=1.0, scale=sc, origin=o2)
            lgA = _mt("A", 36, GOLD).move_to(o2 + 1.3 * np.array([np.cos(ang), np.sin(ang), 0]))
            self.play(*set_alpha(col1, 0.4), *appear(q2, q2b, lag=0.4), run_time=1.4)
            self.play(FadeIn(axes2), GrowArrow(gA), *appear(lgA), run_time=1.0)

            gV = ak.velocity_arrow(0.0, base=0.0, offset=ang, length=1.0, scale=sc, origin=o2)
            ra = ak.right_angle(0.0, at_tip=False, offset=ang, scale=sc, origin=o2, size=0.22)
            va = ang + PI / 2
            lgV = _mt(r"i\omega A", 36, GREEN)
            lgV[0][0].set_color(PINK)
            lgV.move_to(o2 + 2.05 * np.array([np.cos(va), np.sin(va), 0]) + LEFT * 0.45)
            turn = Arc(radius=0.85, start_angle=ang + 0.15, angle=PI / 2 - 0.3, arc_center=o2)
            turn.add_tip(tip_length=0.16).set_stroke(YELLOW, 3)
            turn.get_tip().set_fill(YELLOW).set_stroke(YELLOW)
            xi = _mt(r"\times\, i\omega", 34, YELLOW)
            xi[0][1].set_color(PINK)
            mid = ang + PI / 4
            xi.move_to(o2 + 1.35 * np.array([np.cos(mid), np.sin(mid), 0]) + RIGHT * 0.25)
            c.wait_until("a2")
            self.play(ReplacementTransform(gA.copy(), gV), Create(turn), run_time=1.6)
            self.play(FadeIn(ra), *appear(xi, lgV, lag=0.3), run_time=1.2)
            rule2 = _mt(r"\tfrac{d}{dt} \;\to\; \times\, i\omega", 34)
            rule2[0][-2].set_color(PINK)
            rule2.move_to([COL_X[1], RULE_Y, 0])
            self.play(*appear(rule2), run_time=1.0)

            col2 = [q2, q2b, axes2, gA, lgA, gV, ra, lgV, turn, xi, rule2]

            # q3
            piv = np.array([COL_X[2], 1.2, 0])
            pd = pend.pendulum(theta=25, labels=False, angle=False, pivot=piv, length=1.8)
            u = np.array([np.sin(-25 * DEGREES), -np.cos(25 * DEGREES), 0])
            lL = _mt(r"L = 1\ \mathrm{m}", 32).move_to(piv + 1.0 * u + LEFT * 0.95)
            swing = Arc(radius=1.8, start_angle=-PI / 2 - 25 * DEGREES, angle=50 * DEGREES,
                        arc_center=piv).set_stroke(DIM, 2.5)
            swing = DashedVMobject(swing, num_dashes=12)
            q3 = T("time to swing", size=28).move_to([COL_X[2], Q_Y, 0])
            q3b = T("there and back?", size=28).move_to([COL_X[2], Q2_Y, 0])
            c.wait_until("q3")
            self.play(*set_alpha(col2, 0.4), FadeIn(pd), FadeIn(swing), run_time=1.2)
            self.play(*appear(lL), run_time=0.9)
            c.wait_until(own_word=q3)
            self.play(*appear(q3, q3b, lag=0.4), run_time=1.2)

            ans = _mt(r"T \approx 2\ \mathrm{s}", 40, FG).move_to([COL_X[2], -1.2, 0])
            c.wait_until("a3")
            self.play(*appear(ans), run_time=1.0)

            w_line = _mt(r"\omega = \sqrt{9.81} \approx 3.13\ \mathrm{s}^{-1}", 32)
            w_line.move_to([COL_X[2], -1.9, 0])
            t_line = _mt(r"T = 2\pi/\omega \approx 2.01\ \mathrm{s}", 32)
            t_line[0][2:4].set_color(TEAL)
            t_line.move_to([COL_X[2] + 0.3, -2.6, 0])
            fc = t_line.get_left() + LEFT * 0.42
            a_end = PI / 2 - TAU + 0.5
            ring = Arc(radius=0.22, start_angle=PI / 2, angle=-TAU + 0.5, arc_center=fc).set_stroke(TEAL, 3)
            tip = Triangle().set_fill(TEAL, 1).set_stroke(width=0).scale(0.07)
            tip.rotate(a_end - PI / 2 - PI / 2).move_to(fc + 0.22 * np.array([np.cos(a_end), np.sin(a_end), 0]))
            full = VGroup(ring, tip)
            c.wait_until("omega is")
            self.play(*appear(w_line), run_time=1.0)
            c.wait_until("period is")
            self.play(Create(ring), FadeIn(tip), *appear(t_line), run_time=1.2)
            c.wait_until()
        self.wait(4.5)   # hold the answer before the fade

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
