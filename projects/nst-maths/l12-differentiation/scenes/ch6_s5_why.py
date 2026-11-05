"""Chapter 6, scene 5: why odd and even decide it (Taylor). Clips c6.why.1 – c6.why.5.

Exports:

power_panels() -> VGroup(p2, p3, p4), also .p2 .p3 .p4 and .panels = [p2, p3, p4]
    The three sign panels, static, at this scene's place (centres x = -4.6, 0, 4.6; the GREEN line
    at y = 0.1). Each panel is VGroup(line, curve, dot, title, signs) with parts
      .line    GREEN flat tangent line, 3.6 wide, stroke 4
      .curve   BLUE y = (dx)^n for dx in [-1, 1] (1.6 units per dx horizontally, 1.2 vertically)
      .dot     YELLOW dot at the origin (on the line)
      .title   MathTex "(\\delta x)^n" size 40, \\delta x TEAL, centred 1.7 above the line
      .signs   VGroup(left, right) of YELLOW MathTex size 48 signs: "+","+" (n even), "-","+" (n = 3)
      .n       the power
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

DX = r"\delta x"
PANEL_X = (-4.6, 0.0, 4.6)
PANEL_Y = 0.1
FIG_S = 0.75


def mt(parts, size=44, color=FG, iso=(DX,), colors=None):
    """MathTex, one submobject per part, \\delta x TEAL (plus any extra colours)."""
    parts = parts if isinstance(parts, (list, tuple)) else [parts]
    m = MathTex(*parts, font_size=size, color=color, substrings_to_isolate=list(iso))
    m.set_color_by_tex(DX, TEAL)
    for k, c in (colors or {}).items():
        m.set_color_by_tex(k, c)
    return m


def _panel(n, cx):
    y0 = PANEL_Y
    line = Line([cx - 1.8, y0, 0], [cx + 1.8, y0, 0], color=GREEN, stroke_width=4)
    curve = ParametricFunction(lambda t: np.array([cx + 1.6 * t, y0 + 1.2 * t ** n, 0]),
                               t_range=[-1, 1, 0.01], color=BLUE, stroke_width=5)
    dot = Dot([cx, y0, 0], radius=0.09, color=YELLOW)
    title = mt([r"(\delta x)^" + str(n)], 40).move_to([cx, y0 + 1.7, 0])
    if n % 2 == 0:
        left = MathTex("+", font_size=48, color=YELLOW).move_to([cx - 0.85, y0 + 0.75, 0])
    else:
        left = MathTex("-", font_size=48, color=YELLOW).move_to([cx - 0.85, y0 - 0.75, 0])
    right = MathTex("+", font_size=48, color=YELLOW).move_to([cx + 0.85, y0 + 0.75, 0])
    signs = VGroup(left, right)
    p = VGroup(line, curve, dot, title, signs)
    p.line, p.curve, p.dot, p.title, p.signs, p.n = line, curve, dot, title, signs, n
    return p


def power_panels():
    p2, p3, p4 = (_panel(n, x) for n, x in zip((2, 3, 4), PANEL_X))
    g = VGroup(p2, p3, p4)
    g.p2, g.p3, g.p4 = p2, p3, p4
    g.panels = [p2, p3, p4]
    return g


def _fig():
    s2 = load_scene("ch1_s2_chord")
    f = s2.figure29(dx=0.5, tangent=True, chord=True, braces=True, q_labels=True)
    # δy alone (the long form would collide with the tangent and squeeze the right column)
    f.remove(f.rise_lab, f.tangent_lab)
    f.rise_lab = mt([r"\delta y"], 40, iso=(r"\delta y",), colors={r"\delta y": TEAL})
    f.rise_lab.next_to(f.rise_brace, RIGHT, buff=0.15)
    f.tangent_lab = None
    f.add(f.rise_lab)
    f.add(f.p_dot, f.q_dot)          # dots on top
    f.scale(FIG_S).to_edge(LEFT, buff=0.55)
    f.shift((-0.15 - f.get_center()[1]) * UP)
    f.chord_lab.scale(30 / (34 * FIG_S)).shift(0.3 * RIGHT + 0.1 * DOWN)     # keep the label readable (>= 30) at this scale
    return f


class Why(NarratedScene):
    def construct(self):
        self.quote()
        self.figure()
        self.taylor()
        self.panels()
        self.checks()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # c6.why.1 ---------------------------------------------------------------------------------
    def quote(self):
        with self.say("c6.why.1") as c:
            q = T("“Can I just ask where this odd\nand even will come from?”", 50)
            q.move_to(1.45 * UP)
            qa = T("— a student, after the lecture", 34, DIM)
            qa.next_to(q, DOWN, buff=0.3).align_to(q, RIGHT)
            a = T("“With a Taylor expansion.”", 50).move_to(1.25 * DOWN)
            a.align_to(q, LEFT)
            aa = T("— the lecturer", 34, DIM).next_to(a, DOWN, buff=0.3).align_to(q, RIGHT)
            self.play(*appear(q), run_time=1.0)  # early: the quoted question is shown whole
            c.wait_until(own_word=qa)
            self.play(*appear(qa), run_time=1.0)
            c.wait_until("answer")
            self.play(*appear(aa), run_time=1.0)
            c.wait_until("short")
            self.play(*appear(a), run_time=1.0)  # early: the quote follows the pause after "short"
            self.card = [q, qa, a, aa]

    # c6.why.2 ---------------------------------------------------------------------------------
    def figure(self):
        with self.say("c6.why.2") as c:
            fig = _fig()
            self.fig = fig
            sweep_clear(self, FadeIn(fig), run_time=min(2.0, c.until("def")))
            c.wait_until("def")

            cx = 3.0
            d = mt([r"\dfrac{dy}{dx}", r"\approx", r"\dfrac{y(x + \delta x) - y(x)}{\delta x}"], 44)
            d[0].set_color(GREEN)
            d.move_to([cx, 2.35, 0])
            note = T("δx small, but not yet 0", 30, DIM).next_to(d, DOWN, buff=0.35)
            self.play(*appear(d), run_time=1.2)
            c.wait_until(own_word=note)
            self.play(*appear(note), run_time=1.0)
            c.wait_until("rise")
            self.play(*flash([fig.rise_lab, fig.run_lab]), run_time=1.5)

            c.wait_until("rearrange")
            times = mt([r"\times\, \delta x"], 40, color=YELLOW).next_to(d, RIGHT, buff=0.35)
            self.play(*appear(times), run_time=1.0)

            c.wait_until("eq")
            eq = mt([r"y(x + \delta x)", r"\approx", r"y(x) + \delta x\,\dfrac{dy}{dx}"], 46,
                    iso=(DX, r"\dfrac{dy}{dx}"), colors={r"\dfrac{dy}{dx}": GREEN})
            eq.move_to([cx, -0.45, 0])
            box = SurroundingRectangle(eq, color=YELLOW, buff=0.3, stroke_width=3)
            tag = T("(113)", 28, DIM).next_to(box.get_corner(UR), UP, buff=0.1).align_to(box, RIGHT)
            self.play(*appear(eq), run_time=1.3)
            self.play(FadeIn(box), *appear(tag, shift=None), run_time=0.9)
            c.wait_until("the value of why")
            self.play(*flash([eq[0], fig.q_dot]), run_time=1.3)
            c.wait_until("its value")
            self.play(*flash([eq[2], fig.p_dot]), run_time=1.3)

            # the tangent line's height at x + dx, and the gap to the curve
            c.wait_until("tangent")
            ax = fig.axes
            dxv = ValueTracker(0.5)
            gdot = Dot(ax.c2p(1.5, 2.5), radius=0.09, color=GREEN)
            gap = Line(ax.c2p(1.5, 2.5), ax.c2p(1.5, 3.375), color=YELLOW, stroke_width=7)
            labels = [fig.run_brace, fig.run_lab, fig.rise_brace, fig.rise_lab, fig.run_leg,
                      fig.rise_leg, fig.right_angle, fig.q_lab, fig.chord_lab]
            self.play(*during(disappear(*labels), 0, 0.45),
                      *during([eq[2].animate.set_color(GREEN)], 0.2, 0.8),
                      *during([FadeIn(gap), FadeIn(gdot, scale=0.5)], 0.45, 1.0),
                      run_time=min(1.6, c.until("shrink")))
            fig.remove(*labels)
            settle(self, fig)
            self.remove(gap, gdot)
            self.add(gap, fig.q_dot, gdot)

            # readouts
            rd = VGroup(mt([r"\delta x", "="], 40),
                        DecimalNumber(0.5, num_decimal_places=2, font_size=40, color=TEAL))
            rd.arrange(RIGHT, buff=0.18)
            rg = VGroup(T("gap", 36, YELLOW), MathTex("=", font_size=40),
                        DecimalNumber(0.875, num_decimal_places=3, font_size=40, color=YELLOW))
            rg.arrange(RIGHT, buff=0.18)
            rg[0].align_to(rg[2], DOWN)
            VGroup(rd, rg).arrange(RIGHT, buff=1.0).move_to([cx, -2.45, 0])
            rd[1].add_updater(lambda m: m.set_value(dxv.get_value()))
            rg[2].add_updater(lambda m: m.set_value(3 * dxv.get_value() ** 2 + dxv.get_value() ** 3))

            def upd_q(m):
                x = 1 + dxv.get_value()
                m.move_to(ax.c2p(x, x ** 3))

            def upd_drop(m):
                x = 1 + dxv.get_value()
                m.become(DashedLine(ax.c2p(x, x ** 3), ax.c2p(x, 0), color=DIM, dash_length=0.1 * FIG_S,
                                    stroke_width=3))

            def upd_chord(m):
                P = ax.c2p(1, 1)
                x = 1 + dxv.get_value()
                v = ax.c2p(x, x ** 3) - P
                v = v / np.linalg.norm(v)
                m.become(Line(P - 1.1 * FIG_S * v, P + 4.2 * FIG_S * v, color=TEAL, stroke_width=4))

            def upd_gdot(m):
                x = 1 + dxv.get_value()
                m.move_to(ax.c2p(x, 1 + 3 * (x - 1)))

            def upd_gap(m):
                x = 1 + dxv.get_value()
                m.put_start_and_end_on(ax.c2p(x, 1 + 3 * (x - 1)), ax.c2p(x, x ** 3 + 1e-4))

            c.wait_until("shrink")
            self.play(*appear(rd, rg, lag=0.2), run_time=0.8)
            fig.q_dot.add_updater(upd_q)
            fig.q_drop.add_updater(upd_drop)
            fig.chord.add_updater(upd_chord)
            gdot.add_updater(upd_gdot)
            gap.add_updater(upd_gap)
            self.play(dxv.animate.set_value(0.08), run_time=max(1.0, c.remaining - 0.15),
                      rate_func=linear)
            for m in (fig.q_dot, fig.q_drop, fig.chord, gdot, gap, rd[1], rg[2]):
                m.clear_updaters()
            self.eq = eq
            self.readouts = (rd, rg)
            self.box_tag = (box, tag)

    # c6.why.3 ---------------------------------------------------------------------------------
    def taylor(self):
        with self.say("c6.why.3") as c:
            eq = self.eq
            l1 = mt([r"y(x_0 + \delta x)", "=", r"y(x_0)", "+", r"\delta x\, y'(x_0)"], 46)
            l1.move_to([0, 2.2, 0]).to_edge(LEFT, buff=0.7)
            keep = [eq] + list(self.readouts)
            others = [m for m in self.mobjects if m not in keep]
            self.play(*during(disappear(*others), 0, 0.5),
                      *during([eq.animate.move_to(l1)], 0.35, 1.0),
                      run_time=1.6)
            self.play(*edit(eq, l1), *disappear(*self.readouts), run_time=1.5)

            ts = T("Taylor series", 40, YELLOW).next_to(l1, UP, buff=0.45).align_to(l1, LEFT)
            c.wait_until(own_word=ts)
            self.play(*appear(ts), run_time=1.0)

            ta = mt(["+", r"\dfrac{(\delta x)^2}{2!}\, y''(x_0)"], 44)
            ta.next_to(l1[2], DOWN, buff=0).align_to(l1[2], LEFT)
            ta.set_y(0.3)
            tb = mt(["+", r"\dfrac{(\delta x)^3}{3!}\, y'''(x_0)", "+", r"\cdots"], 44)
            tb.next_to(ta, RIGHT, buff=0.2)
            c.wait_until("sq")
            self.play(*appear(ta), run_time=1.3)
            c.wait_until("cube")
            self.play(*appear(tb), run_time=1.3)

            # stationary point
            c.wait_until("stat")
            sline = Line(LEFT * 0.9, RIGHT * 0.9, color=GREEN, stroke_width=4)
            sdot = Dot(radius=0.09, color=YELLOW)
            icon = VGroup(sline, sdot).move_to([4.2, 2.6, 0])
            slab = VGroup(T("stationary point at", 30, DIM), MathTex("x_0", font_size=36, color=DIM))
            slab.arrange(RIGHT, buff=0.15)
            slab[1].align_to(slab[0], DOWN).shift(0.04 * DOWN)
            slab.next_to(icon, DOWN, buff=0.3)
            self.play(FadeIn(icon), *appear(slab[0], slab[1], lag=0), run_time=1.0)

            c.wait_until("gone")
            zero = MathTex(r"y'(x_0) = 0", font_size=36, color=FG).next_to(l1[4], DOWN, buff=0.3)
            self.play(*appear(zero), *recolor([l1[3], l1[4]], DIM), run_time=1.2)

            # the general term
            c.wait_until("first")
            tb2 = mt(["+", r"\cdots", "+", r"\dfrac{(\delta x)^n}{n!}\, y^{(n)}(x_0)", "+", r"\cdots"], 44)
            tb2.move_to(tb).align_to(tb, LEFT)
            self.play(*edit(tb, tb2), run_time=1.5)
            c.wait_until("zero too")
            self.play(*recolor([ta, tb2[0], tb2[1], tb2[2]], DIM), *flash([tb2[3]]), run_time=1.3)

            c.wait_until("small")
            tiny = T("higher powers of δx: tiny", 30, DIM)
            tiny.next_to(tb2, DOWN, buff=0.35).align_to(tb2, RIGHT)
            self.play(*set_alpha([tb2[4], tb2[5]], 0.5), *appear(tiny), run_time=1.0)

            # the leading term
            c.wait_until("the change")
            res = mt([r"y(x_0 + \delta x) - y(x_0)", r"\approx", r"\dfrac{(\delta x)^n}{n!}\, y^{(n)}(x_0)"],
                     46)
            res.move_to([0, -2.1, 0])
            rbox = SurroundingRectangle(res, color=YELLOW, buff=0.25, stroke_width=3)
            self.play(*appear(res), run_time=1.3)
            hl = T("height above the flat tangent line", 30, DIM)
            hl.next_to(rbox, DOWN, buff=0.15).align_to(res, LEFT)
            self.play(FadeIn(rbox), *appear(hl), run_time=1.0)  # early: names the left side; its words aren't spoken
            self.res, self.rbox, self.hl = res, rbox, hl

    # c6.why.4 ---------------------------------------------------------------------------------
    def panels(self):
        with self.say("c6.why.4") as c:
            res, rbox = self.res, self.rbox
            lead = VGroup(res, rbox)
            settle(self, lead)
            others = [m for m in self.mobjects if m is not lead and m is not self.hl]
            self.play(*during(disappear(*others), 0, 0.5),
                      *during([lead.animate.scale(0.75).move_to([0, 2.95, 0])], 0.3, 1.0),
                      run_time=1.4)
            pp = power_panels()
            for p in pp.panels:
                p.remove(p.signs)
            self.play(*disappear(self.hl), *appear(*pp.panels, lag=0.3), run_time=1.5)
            self.play(*flash([res[2]]), run_time=1.0)
            p2, p3, p4 = pp.panels

            c.wait_until("even")
            self.play(*appear(p2.signs[0], p2.signs[1], p4.signs[0], p4.signs[1], shift=None, lag=0.2),
                      run_time=1.3)

            c.wait_until("evenmin")
            self.play(VShowPassingFlash(p2.curve.copy().set_stroke(YELLOW, 8), time_width=0.5),
                      VShowPassingFlash(p4.curve.copy().set_stroke(YELLOW, 8), time_width=0.5),
                      run_time=1.6)
            mins = [T("minimum", 32, YELLOW).move_to([p.line.get_center()[0], -1.75, 0]) for p in (p2, p4)]
            c.wait_until(own_word=mins[0])
            self.play(*appear(*mins, lag=0), run_time=1.0)

            c.wait_until("evenmax")
            ghosts, flips = [], []
            for p in (p2, p4):
                g = p.curve.copy().set_stroke(BLUE, 5, opacity=0.45)
                f = g.copy().apply_function(lambda q: np.array([q[0], 2 * PANEL_Y - q[1], 0]))
                ghosts.append(g)
                flips.append(f)
            self.add(*ghosts)
            self.play(*[Transform(g, f) for g, f in zip(ghosts, flips)], run_time=1.6)
            maxs = [MathTex(r"\text{maximum (negative } y^{(n)})", font_size=32, color=YELLOW)
                    .move_to([p.line.get_center()[0], -2.45, 0]) for p in (p2, p4)]
            c.wait_until("a maximum")
            self.play(*appear(*maxs, lag=0), run_time=1.0)
            self.ghosts, self.maxs = ghosts, maxs
            c.wait_until("odd")
            self.play(*appear(p3.signs[0], p3.signs[1], shift=None, lag=0.4), run_time=1.4)

            c.wait_until("cross")
            self.play(VShowPassingFlash(p3.curve.copy().set_stroke(YELLOW, 8), time_width=0.5),
                      run_time=1.6)
            infl = T("point of inflection", 32, YELLOW).move_to([p3.line.get_center()[0], -1.75, 0])
            c.wait_until(own_word=infl)
            self.play(*appear(infl), run_time=1.0)
            self.pp = pp

    # c6.why.5 ---------------------------------------------------------------------------------
    def checks(self):
        with self.say("c6.why.5") as c:
            p2, p3, p4 = self.pp.panels
            c4 = MathTex(r"y = x^4:\quad", r"\dfrac{24}{4!}", "= 1", font_size=38)
            c4[1].set_color(GOLD)
            c4.move_to([p4.line.get_center()[0], -2.75, 0])
            self.play(*during(disappear(*self.ghosts, *self.maxs), 0, 0.45),
                      *during(appear(c4), 0.45, 1.0), run_time=1.6)
            c.wait_until("so the change")
            self.play(*flash([p4.title]), run_time=1.5)

            c.wait_until("cubecheck")
            c3 = MathTex(r"y = x^3:\quad", r"\dfrac{6}{3!}", "= 1", font_size=38)
            c3[1].set_color(GOLD)
            c3.move_to([p3.line.get_center()[0], -2.75, 0])
            self.play(*appear(c3), run_time=1.2)
            c.wait_until("negative on the left")
            self.play(*flash([p3.signs[0]]), run_time=1.2)
            c.wait_until("positive on the right")
            self.play(*flash([p3.signs[1]]), run_time=1.2)
